"""Formato de texto del recorrido RAG."""
from __future__ import annotations

from src.rag import Hit


def bloque_hits(hits: list[Hit]) -> str:
    lineas = []
    for h in hits:
        lineas.append(
            f"    {h.rango}. [{h.chunk.id}] {h.chunk.titulo}  "
            f"score={h.score:.3f}  ({h.chunk.fuente})"
        )
        lineas.append(f"       {h.chunk.texto[:160]}")
    return "\n".join(lineas) if lineas else "    (nada)"


def walkthrough(correo: str, pred: str | None, retriever: str, hits: list[Hit], prompt: str, respuesta: str) -> str:
    pred_txt = pred if pred is not None else "(sin clasificador)"
    return f"""
============================================================
UN CORREO RECORRE EL SISTEMA
============================================================

CORREO
------
{correo}

EJE 1 — predicción
------------------
{pred_txt}

EJE 2 — retriever = {retriever}
-------------------------------
Fragmentos recuperados:
{bloque_hits(hits)}

PROMPT QUE SE LE ENVÍA AL LLM
-----------------------------
{prompt}

RESPUESTA
---------
{respuesta}
""".strip() + "\n"
