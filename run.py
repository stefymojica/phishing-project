#!/usr/bin/env python3
"""
Punto de entrada. Desde esta carpeta:

    python run.py              # demo + eje 1 + eje 2
    python run.py demo
    python run.py eje1
    python run.py eje2
    python run.py eje2 --llm ollama --model gemma2:2b
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from experiments import run_demo, run_eje1, run_eje2  # noqa: E402


def parse_args(argv: list[str] | None = None):
    p = argparse.ArgumentParser(description="Detección de phishing: clasificación + RAG")
    p.add_argument("comando", nargs="?", default="todo", choices=["todo", "demo", "eje1", "eje2"])
    p.add_argument("--llm", default="auto", choices=["auto", "extractivo", "ollama"],
                   help="auto = Gemma 2B si Ollama está arriba; si no, extractivo")
    p.add_argument("--model", default="gemma2:2b", help="nombre del modelo en Ollama")
    p.add_argument("--k", type=int, default=3, help="cuántos fragmentos recupera el RAG")
    p.add_argument("--no-sbert", action="store_true", help="no uses sentence-transformers")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    sbert = not args.no_sbert
    print(f"comando={args.comando}  llm={args.llm}  k={args.k}")

    if args.comando in ("todo", "demo"):
        run_demo(llm=args.llm, modelo=args.model, k=args.k)
    if args.comando in ("todo", "eje1"):
        run_eje1(incluir_sbert=sbert)
    if args.comando in ("todo", "eje2"):
        run_eje2(llm=args.llm, modelo=args.model, k=args.k, incluir_sbert=sbert)

    print("\nListo. Tablas y el recorrido del RAG están en experiments/results/")


if __name__ == "__main__":
    main()
