"""Un solo correo: clasificador + LLM solo vs RAG+LLM."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.classify import modelos
from src.config import OLLAMA_MODEL, RESULTS_DIR, TOP_K, ensure_dirs
from src.data import knowledge_base, load_dataset
from src.embeddings import TfidfEmb, a_densa
from src.rag import Indice, generar, generar_sin_rag, ollama_disponible, resolver_modelo
from src.report import walkthrough

CORREO_ID = "p25"  # Microsoft 365 falso, está en test


def run(llm: str = "auto", modelo: str = OLLAMA_MODEL, k: int = TOP_K):
    train, test, positiva = load_dataset()
    row = test[test["id"] == CORREO_ID].iloc[0]
    correo = row["text"]

    emb = TfidfEmb().fit(train["text"].tolist())
    svm = modelos()["SVM"]
    svm.fit(a_densa(emb.transform(train["text"].tolist())), train["label"].tolist())
    pred = svm.predict(a_densa(emb.transform([correo])))[0]

    chunks = knowledge_base(train, incluir_correos_train=False)
    indice = Indice("bm25", chunks)
    hits = indice.retrieve(correo, k=k)

    hay_llm = ollama_disponible()
    if llm == "auto":
        llm = "ollama" if hay_llm else "extractivo"
    modelo_real = resolver_modelo(modelo) if llm == "ollama" else modelo
    print(f"\nLLM = {llm}  modelo = {modelo_real}  ollama={'sí' if hay_llm else 'no'}")

    prompt, respuesta = generar(correo, hits, llm=llm, modelo=modelo_real)
    texto = walkthrough(
        correo,
        f"SVM + TF-IDF → {pred}  (clase positiva: {positiva})",
        "bm25",
        hits,
        prompt,
        respuesta,
    )

    if llm == "ollama" and hay_llm:
        prompt_solo, resp_solo = generar_sin_rag(correo, modelo=modelo_real)
        extra = f"""
============================================================
MISMO CORREO, LLM SIN RAG
============================================================

PROMPT
------
{prompt_solo}

RESPUESTA SIN BASE
------------------
{resp_solo}

La diferencia: con RAG tiene que citar [campana_microsoft] / [regla_urgencia].
Sin RAG puede nombrar campañas que no están en la base.
"""
        texto = texto + "\n" + extra.strip() + "\n"

    print("\n" + texto)
    ensure_dirs()
    path = RESULTS_DIR / "demo.md"
    path.write_text(texto, encoding="utf-8")
    print(f"Demo guardada → {path}")
    return pred, hits, respuesta


if __name__ == "__main__":
    run()
