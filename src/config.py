"""Rutas, semilla, hiperparámetros y constantes de Ollama."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "experiments" / "results"
OUTPUTS_DIR = ROOT / "outputs"

EMAILS_CSV = DATA_DIR / "emails.csv"
REGLAS_JSON = DATA_DIR / "knowledge_base" / "reglas.json"
CAMPANAS_JSON = DATA_DIR / "knowledge_base" / "campanas.json"
PREGUNTAS_JSON = DATA_DIR / "eval" / "preguntas.json"

RANDOM_STATE = 0
TOP_K = 3

# Word2Vec / GloVe
VECTOR_SIZE = 50
WINDOW = 5
W2V_EPOCHS = 40

TFIDF_MAX_FEATURES = 3000

# Ollama (Gemma 2B, local)
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_TAGS = "http://localhost:11434/api/tags"
OLLAMA_MODEL = "gemma2:2b"


def ensure_dirs() -> None:
    for path in (DATA_DIR, RESULTS_DIR, OUTPUTS_DIR, REGLAS_JSON.parent, PREGUNTAS_JSON.parent):
        path.mkdir(parents=True, exist_ok=True)
