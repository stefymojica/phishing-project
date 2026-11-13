"""Detección de phishing: clasificación (eje 1) y explicación con RAG (eje 2)."""
import warnings

# NumPy 2 + sklearn en macOS imprime overflow en matmul aunque el resultado sirva.
warnings.filterwarnings("ignore", message=".*encountered in matmul")
warnings.filterwarnings("ignore", category=FutureWarning, module=r"sklearn\.ensemble\._weight_boosting")
