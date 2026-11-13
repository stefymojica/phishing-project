"""Gráficos del informe."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import pandas as pd

from src.config import OUTPUTS_DIR, ensure_dirs


def barras_f1(df: pd.DataFrame, archivo: str = "f1_clasificacion.png") -> None:
    ensure_dirs()
    import matplotlib.pyplot as plt

    tabla = df.pivot_table(index="embedding", columns="modelo", values="f1")
    ax = tabla.plot(kind="bar", figsize=(9, 4.5), rot=0)
    ax.set_ylabel("F1 (clase phishing)")
    ax.set_title("Eje 1. F1 de phishing según representación y modelo")
    ax.legend(title="modelo", loc="lower right")
    ax.set_ylim(0, 1.05)
    plt.tight_layout()
    path = OUTPUTS_DIR / archivo
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"Gráfico → {path}")


def barras_rag(df: pd.DataFrame, archivo: str = "rag_recall.png") -> None:
    ensure_dirs()
    import matplotlib.pyplot as plt

    ax = df.plot(x="retriever", y=["recall@k", "mrr"], kind="bar", figsize=(8, 4), rot=0)
    ax.set_ylim(0, 1.05)
    ax.set_title("Eje 2. Recall@3 y MRR por retriever")
    plt.tight_layout()
    path = OUTPUTS_DIR / archivo
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"Gráfico → {path}")
