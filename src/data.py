"""Carga de correos y de la base de conocimiento del RAG."""
from __future__ import annotations

import json
from dataclasses import dataclass

import pandas as pd

from src import corpus
from src.config import (
    CAMPANAS_JSON,
    EMAILS_CSV,
    PREGUNTAS_JSON,
    REGLAS_JSON,
    ensure_dirs,
)
from src.text import juntar_correo


@dataclass
class Chunk:
    id: str
    titulo: str
    texto: str
    fuente: str  # regla | campana | correo_train

    def as_text(self) -> str:
        return f"{self.titulo}. {self.texto}"


def exportar_sample() -> pd.DataFrame:
    """Exporta el corpus a CSV/JSON en data/."""
    ensure_dirs()
    df = pd.DataFrame(corpus.EMAILS)
    df.to_csv(EMAILS_CSV, index=False)
    REGLAS_JSON.write_text(json.dumps(corpus.REGLAS, ensure_ascii=False, indent=2), encoding="utf-8")
    CAMPANAS_JSON.write_text(json.dumps(corpus.CAMPANAS, ensure_ascii=False, indent=2), encoding="utf-8")
    PREGUNTAS_JSON.write_text(json.dumps(corpus.PREGUNTAS, ensure_ascii=False, indent=2), encoding="utf-8")
    return df


def load_dataset() -> tuple[pd.DataFrame, pd.DataFrame, str]:
    df = exportar_sample()
    df["text"] = [juntar_correo(s, b) for s, b in zip(df["subject"], df["body"])]
    train = df[df["split"] == "train"].reset_index(drop=True)
    test = df[df["split"] == "test"].reset_index(drop=True)
    return train, test, "phishing"


def knowledge_base(train: pd.DataFrame | None = None, incluir_correos_train: bool = True) -> list[Chunk]:
    """Fragmentos que el RAG puede citar: reglas, campañas y, si se pide, phishing de train."""
    exportar_sample()
    chunks: list[Chunk] = []
    for row in json.loads(REGLAS_JSON.read_text(encoding="utf-8")):
        chunks.append(Chunk(row["id"], row["titulo"], row["texto"], "regla"))
    for row in json.loads(CAMPANAS_JSON.read_text(encoding="utf-8")):
        chunks.append(Chunk(row["id"], row["titulo"], row["texto"], "campana"))
    if incluir_correos_train and train is not None:
        pos = train[train["label"] == "phishing"]
        for _, row in pos.iterrows():
            texto = juntar_correo(row.get("subject", ""), row.get("body", row.get("text", "")))
            chunks.append(
                Chunk(
                    id=f"correo_{row['id']}",
                    titulo=f"Caso conocido ({row['id']})",
                    texto=texto,
                    fuente="correo_train",
                )
            )
    return chunks


def load_preguntas(test: pd.DataFrame) -> list[dict]:
    exportar_sample()
    preguntas = json.loads(PREGUNTAS_JSON.read_text(encoding="utf-8"))
    by_id = {row["id"]: row for _, row in test.iterrows()}
    out = []
    for q in preguntas:
        if q["email_id"] not in by_id:
            continue
        row = by_id[q["email_id"]]
        out.append({**q, "text": juntar_correo(row["subject"], row["body"]), "label": row["label"]})
    return out
