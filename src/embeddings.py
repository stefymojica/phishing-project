"""Representaciones de texto para el eje 1 y para recuperar fragmentos en el eje 2."""
from __future__ import annotations

import numpy as np
from scipy.sparse import lil_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

from src.config import TFIDF_MAX_FEATURES, VECTOR_SIZE, W2V_EPOCHS, WINDOW
from src.text import tokenize


def _promedio_palabras(docs: list[str], vectores: dict[str, np.ndarray], dim: int) -> np.ndarray:
    filas = []
    for doc in docs:
        toks = [t for t in tokenize(doc) if t in vectores]
        if not toks:
            filas.append(np.zeros(dim, dtype=np.float32))
        else:
            filas.append(np.mean([vectores[t] for t in toks], axis=0))
    return np.vstack(filas)


class TfidfEmb:
    nombre = "tfidf"

    def __init__(self) -> None:
        self.vec = TfidfVectorizer(max_features=TFIDF_MAX_FEATURES, token_pattern=r"[a-záéíóúñü0-9]+")

    def fit(self, texts: list[str]) -> "TfidfEmb":
        self.vec.fit(texts)
        return self

    def transform(self, texts: list[str]) -> np.ndarray:
        return self.vec.transform(texts)


class Word2VecEmb:
    """CBOW (sg=0) o Skip-gram (sg=1), promedio de vectores de palabra."""

    def __init__(self, sg: int) -> None:
        self.sg = sg
        self.nombre = "skipgram" if sg == 1 else "cbow"
        self.kv: dict[str, np.ndarray] = {}
        self.dim = VECTOR_SIZE

    def fit(self, texts: list[str]) -> "Word2VecEmb":
        from gensim.models import Word2Vec

        oraciones = [tokenize(t) for t in texts]
        oraciones = [o if o else ["<vacio>"] for o in oraciones]
        modelo = Word2Vec(
            sentences=oraciones,
            vector_size=self.dim,
            window=WINDOW,
            min_count=1,
            sg=self.sg,
            epochs=W2V_EPOCHS,
            workers=1,
            seed=0,
        )
        self.kv = {w: modelo.wv[w] for w in modelo.wv.index_to_key}
        return self

    def transform(self, texts: list[str]) -> np.ndarray:
        return _promedio_palabras(texts, self.kv, self.dim)


class GloveSvdEmb:
    """GloVe: matriz de co-ocurrencia global, log1p y SVD."""

    nombre = "glove"

    def __init__(self) -> None:
        self.kv: dict[str, np.ndarray] = {}
        self.dim = VECTOR_SIZE

    def fit(self, texts: list[str]) -> "GloveSvdEmb":
        docs = [tokenize(t) for t in texts]
        vocab = sorted({w for doc in docs for w in doc}) or ["<vacio>"]
        idx = {w: i for i, w in enumerate(vocab)}
        n = len(vocab)
        C = lil_matrix((n, n), dtype=np.float64)
        for doc in docs:
            for i, w in enumerate(doc):
                for j in range(max(0, i - WINDOW), min(len(doc), i + WINDOW + 1)):
                    if i == j:
                        continue
                    C[idx[w], idx[doc[j]]] += 1.0 / abs(i - j)
        denso = np.log1p(C.tocsr().toarray())
        k = min(self.dim, max(1, min(denso.shape) - 1))
        algo = "arpack" if min(denso.shape) <= 500 else "randomized"
        svd = TruncatedSVD(n_components=k, random_state=0, algorithm=algo)
        vecs = svd.fit_transform(denso)
        self.kv = {w: vecs[i] for w, i in idx.items()}
        self.dim = k
        return self

    def transform(self, texts: list[str]) -> np.ndarray:
        return _promedio_palabras(texts, self.kv, self.dim)


class SbertEmb:
    """Sentence-transformers (opcional)."""

    nombre = "sbert"
    MODELO = "paraphrase-multilingual-MiniLM-L12-v2"

    def __init__(self) -> None:
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(self.MODELO)

    def fit(self, texts: list[str]) -> "SbertEmb":
        return self

    def transform(self, texts: list[str]) -> np.ndarray:
        return np.asarray(self.model.encode(texts, show_progress_bar=False, normalize_embeddings=True))


def construir(nombre: str):
    if nombre == "tfidf":
        return TfidfEmb()
    if nombre == "cbow":
        return Word2VecEmb(sg=0)
    if nombre == "skipgram":
        return Word2VecEmb(sg=1)
    if nombre == "glove":
        return GloveSvdEmb()
    if nombre == "sbert":
        return SbertEmb()
    raise ValueError(f"Embedding desconocido: {nombre}")


def disponibles(incluir_sbert: bool = True) -> list[str]:
    nombres = ["tfidf", "cbow", "skipgram", "glove"]
    if not incluir_sbert:
        return nombres
    try:
        import sentence_transformers  # noqa: F401

        nombres.append("sbert")
    except ImportError:
        print("sentence-transformers no está instalado: se omite sbert (opcional).")
    return nombres


def a_densa(X) -> np.ndarray:
    if hasattr(X, "toarray"):
        return np.asarray(X.toarray(), dtype=np.float32)
    X = np.asarray(X, dtype=np.float32)
    return normalize(X)
