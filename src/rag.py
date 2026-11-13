"""RAG: recuperar fragmentos, armar el prompt y generar la explicación."""
from __future__ import annotations

import json
import math
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from src.config import OLLAMA_MODEL, OLLAMA_TAGS, OLLAMA_URL, TOP_K
from src.data import Chunk
from src.embeddings import a_densa, construir
from src.text import tokenize


@dataclass
class Hit:
    chunk: Chunk
    score: float
    rango: int


def armar_prompt(correo: str, hits: list[Hit]) -> str:
    bloques = []
    for h in hits:
        bloques.append(f"[{h.chunk.id}] {h.chunk.titulo}\n{h.chunk.texto}")
    fragmentos = "\n\n".join(bloques) if bloques else "(no se recuperó nada)"
    return (
        "Eres analista de phishing. Responde en español, 4 a 8 oraciones.\n"
        "Usando SOLO los fragmentos de abajo, explica si el correo es phishing y por qué.\n"
        "Cita los IDs entre corchetes, por ejemplo [regla_urgencia].\n"
        "Si los fragmentos no alcanzan, responde exactamente: evidencia insuficiente.\n"
        "No inventes campañas, bancos ni URLs que no aparezcan en los fragmentos.\n\n"
        f"CORREO:\n{correo}\n\n"
        f"FRAGMENTOS:\n{fragmentos}\n"
    )


def armar_prompt_sin_rag(correo: str) -> str:
    """Prompt del correo sin fragmentos de la base."""
    return (
        "Eres analista de phishing. Responde en español, 4 a 8 oraciones.\n"
        "Explica si este correo es phishing y por qué.\n"
        "Si se parece a alguna campaña conocida, nómbrala.\n\n"
        f"CORREO:\n{correo}\n"
    )


def generar_extractivo(correo: str, hits: list[Hit]) -> str:
    """Explicación a partir de los fragmentos, sin LLM."""
    if not hits:
        return "evidencia insuficiente"
    lineas = [
        "Explicación extractiva (no usa LLM): el correo se parece a estos fragmentos.",
        "Si el clasificador del eje 1 dijo phishing, estas son las pistas citables:",
        "",
    ]
    for h in hits:
        lineas.append(f"- [{h.chunk.id}] {h.chunk.titulo} (score={h.score:.3f}): {h.chunk.texto}")
    return "\n".join(lineas)


def ollama_disponible() -> bool:
    try:
        with urllib.request.urlopen(OLLAMA_TAGS, timeout=2) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return bool(data.get("models"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return False


def resolver_modelo(preferido: str) -> str:
    try:
        with urllib.request.urlopen(OLLAMA_TAGS, timeout=2) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        nombres = [m.get("name", "") for m in data.get("models", [])]
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return preferido
    if preferido in nombres:
        return preferido
    base = preferido.split(":")[0]
    for n in nombres:
        if n == base or n.startswith(base + ":"):
            return n
    return preferido


def generar_ollama(prompt: str, modelo: str = OLLAMA_MODEL) -> str:
    modelo = resolver_modelo(modelo)
    cuerpo = json.dumps(
        {
            "model": modelo,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2, "num_predict": 280},
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=cuerpo,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return (data.get("response") or "").strip() or "evidencia insuficiente"
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return (
            f"[Ollama no respondió: {exc}]\n"
            "Prueba: ollama serve  &&  ollama pull gemma2:2b\n"
            "Se usa la explicación extractiva como respaldo.\n"
        )


def generar(correo: str, hits: list[Hit], llm: str, modelo: str) -> tuple[str, str]:
    prompt = armar_prompt(correo, hits)
    if llm == "auto":
        llm = "ollama" if ollama_disponible() else "extractivo"
    if llm == "ollama":
        texto = generar_ollama(prompt, modelo=modelo)
        if texto.startswith("[Ollama no respondió"):
            texto = texto + "\n" + generar_extractivo(correo, hits)
        return prompt, texto
    return prompt, generar_extractivo(correo, hits)


def generar_sin_rag(correo: str, modelo: str = OLLAMA_MODEL) -> tuple[str, str]:
    prompt = armar_prompt_sin_rag(correo)
    return prompt, generar_ollama(prompt, modelo=modelo)


class BM25:
    """Okapi BM25."""

    nombre = "bm25"

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.docs: list[list[str]] = []
        self.df: Counter = Counter()
        self.avgdl = 0.0

    def fit(self, texts: list[str]) -> "BM25":
        self.docs = [tokenize(t) for t in texts]
        self.df = Counter()
        for doc in self.docs:
            self.df.update(set(doc))
        self.avgdl = sum(len(d) for d in self.docs) / max(1, len(self.docs))
        return self

    def scores(self, query: str) -> np.ndarray:
        q = tokenize(query)
        n = len(self.docs)
        out = np.zeros(n, dtype=np.float32)
        for i, doc in enumerate(self.docs):
            tf = Counter(doc)
            dl = len(doc) or 1
            s = 0.0
            for term in q:
                if term not in tf:
                    continue
                idf = math.log((n - self.df[term] + 0.5) / (self.df[term] + 0.5) + 1)
                denom = tf[term] + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
                s += idf * (tf[term] * (self.k1 + 1) / denom)
            out[i] = s
        return out


class Indice:
    """Retriever sobre los fragmentos de la base."""

    def __init__(self, nombre: str, chunks: list[Chunk]) -> None:
        self.nombre = nombre
        self.chunks = chunks
        self.textos = [c.as_text() for c in chunks]
        self._bm25: BM25 | None = None
        self._emb = None
        self._M = None
        if nombre == "bm25":
            self._bm25 = BM25().fit(self.textos)
        else:
            self._emb = construir(nombre)
            corpus_fit = self.textos[:]
            self._emb.fit(corpus_fit)
            self._M = a_densa(self._emb.transform(self.textos))

    def retrieve(self, query: str, k: int = TOP_K) -> list[Hit]:
        if self._bm25 is not None:
            scores = self._bm25.scores(query)
        else:
            q = a_densa(self._emb.transform([query]))
            scores = cosine_similarity(q, self._M)[0]
        orden = np.argsort(-scores)[:k]
        return [
            Hit(chunk=self.chunks[i], score=float(scores[i]), rango=r + 1)
            for r, i in enumerate(orden)
        ]


def construir_indices(chunks: list[Chunk], nombres: list[str]) -> dict[str, Indice]:
    indices = {}
    for nombre in nombres:
        print(f"  índice RAG: {nombre} ({len(chunks)} chunks)")
        indices[nombre] = Indice(nombre, chunks)
    return indices
