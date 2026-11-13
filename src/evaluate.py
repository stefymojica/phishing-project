"""Métricas y tablas."""
from __future__ import annotations

import json

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.config import RESULTS_DIR, ensure_dirs


def metricas_clasificacion(y_true, y_pred, etiqueta_positiva: str) -> dict:
    return {
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred, pos_label=etiqueta_positiva, zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, pos_label=etiqueta_positiva, zero_division=0), 4),
        "f1": round(f1_score(y_true, y_pred, pos_label=etiqueta_positiva, zero_division=0), 4),
    }


def recall_at_k(gold: list[str], retrieved: list[str]) -> float:
    if not gold:
        return 0.0
    got = set(retrieved)
    return sum(1 for g in gold if g in got) / len(gold)


def mrr(gold: list[str], retrieved: list[str]) -> float:
    for i, cid in enumerate(retrieved, start=1):
        if cid in gold:
            return 1.0 / i
    return 0.0


def guardar_tabla(filas: list[dict], nombre: str) -> pd.DataFrame:
    ensure_dirs()
    df = pd.DataFrame(filas)
    csv_path = RESULTS_DIR / f"{nombre}.csv"
    md_path = RESULTS_DIR / f"{nombre}.md"
    df.to_csv(csv_path, index=False)
    md_path.write_text(_a_markdown(df), encoding="utf-8")
    print(f"Tabla → {csv_path}")
    return df


def guardar_json(obj, nombre: str) -> None:
    ensure_dirs()
    path = RESULTS_DIR / f"{nombre}.json"
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"JSON  → {path}")


def _a_markdown(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lineas = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for _, row in df.iterrows():
        lineas.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
    return "\n".join(lineas) + "\n"
