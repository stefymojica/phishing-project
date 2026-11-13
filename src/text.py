"""Tokenización."""
from __future__ import annotations

import re

TOKEN = re.compile(r"[a-záéíóúñü0-9]+", re.IGNORECASE)


def tokenize(text: str) -> list[str]:
    return TOKEN.findall((text or "").lower())


def juntar_correo(subject: str, body: str) -> str:
    return f"{subject or ''}\n{body or ''}".strip()
