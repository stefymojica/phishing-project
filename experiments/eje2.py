"""Eje 2: mismo correo, distintos retrievers, mismo generador."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import OLLAMA_MODEL, RESULTS_DIR, TOP_K, ensure_dirs
from src.data import knowledge_base, load_dataset, load_preguntas
from src.embeddings import disponibles
from src.evaluate import guardar_json, guardar_tabla, mrr, recall_at_k
from src.plots import barras_rag
from src.rag import construir_indices, generar, generar_sin_rag, ollama_disponible, resolver_modelo
from src.report import walkthrough


def run(llm: str = "auto", modelo: str = OLLAMA_MODEL, k: int = TOP_K, incluir_sbert: bool = True):
    train, test, _ = load_dataset()
    # Solo reglas y campañas.
    chunks = knowledge_base(train, incluir_correos_train=False)
    preguntas = load_preguntas(test)
    if llm == "auto":
        llm = "ollama" if ollama_disponible() else "extractivo"
    modelo = resolver_modelo(modelo) if llm == "ollama" else modelo
    print(f"\nEje 2 — chunks={len(chunks)}  preguntas={len(preguntas)}  k={k}  llm={llm}  modelo={modelo}")

    nombres = ["bm25"] + disponibles(incluir_sbert=incluir_sbert)
    indices = construir_indices(chunks, nombres)

    filas = []
    ejemplos = []
    for nombre, indice in indices.items():
        recs, mrrs = [], []
        for q in preguntas:
            hits = indice.retrieve(q["text"], k=k)
            ids = [h.chunk.id for h in hits]
            recs.append(recall_at_k(q["gold_chunk_ids"], ids))
            mrrs.append(mrr(q["gold_chunk_ids"], ids))
            # Retrieval; el LLM se llama en el recorrido (pregunta 1).
            ejemplos.append({
                "pregunta": q["id"],
                "retriever": nombre,
                "email_id": q["email_id"],
                "gold": q["gold_chunk_ids"],
                "recuperado": ids,
                "recall_at_k": recs[-1],
            })
        fila = {
            "retriever": nombre,
            "recall@k": round(sum(recs) / len(recs), 4) if recs else 0.0,
            "mrr": round(sum(mrrs) / len(mrrs), 4) if mrrs else 0.0,
            "n": len(preguntas),
        }
        filas.append(fila)
        print(f"  {nombre:12}  Recall@{k}={fila['recall@k']:.3f}  MRR={fila['mrr']:.3f}")

    df = guardar_tabla(filas, "rag_retrieval")
    guardar_json(ejemplos, "rag_ejemplos")
    _escribir_md(preguntas, indices, llm, modelo, k)
    if not df.empty:
        barras_rag(df)
    return df


def _escribir_md(preguntas, indices, llm, modelo, k) -> None:
    """Escribe prompt, fragmentos y respuesta en markdown."""
    ensure_dirs()
    partes = ["# Eje 2 — recorrido RAG\n", f"llm={llm}  modelo={modelo}  k={k}\n"]
    # una pregunta, todos los retrievers
    q = preguntas[0]
    partes.append(f"\n## Ejemplo largo: {q['id']} ({q['email_id']})\n")
    partes.append(q["text"] + "\n")
    partes.append(f"gold: {q['gold_chunk_ids']}\n")
    if llm == "ollama":
        print("  Gemma sin RAG (mismo correo, sin fragmentos)...")
        p_solo, r_solo = generar_sin_rag(q["text"], modelo=modelo)
        partes.append("\n### LLM sin RAG\n\n")
        partes.append(p_solo + "\n\n")
        partes.append(r_solo + "\n")
    for nombre, indice in indices.items():
        print(f"  Gemma + RAG retriever={nombre}...")
        hits = indice.retrieve(q["text"], k=k)
        prompt, respuesta = generar(q["text"], hits, llm=llm, modelo=modelo)
        partes.append(walkthrough(q["text"], None, nombre, hits, prompt, respuesta))
        partes.append("\n")
    partes.append("\n## Las demás preguntas (solo IDs recuperados)\n")
    for q in preguntas[1:]:
        partes.append(f"\n### {q['id']}  gold={q['gold_chunk_ids']}\n")
        partes.append(q["text"] + "\n")
        for nombre, indice in indices.items():
            hits = indice.retrieve(q["text"], k=k)
            partes.append(f"- **{nombre}**: " + ", ".join(f"{h.chunk.id}({h.score:.2f})" for h in hits))
            partes.append("\n")
    path = RESULTS_DIR / "rag_recorrido.md"
    path.write_text("".join(partes), encoding="utf-8")
    print(f"Recorrido RAG → {path}")


if __name__ == "__main__":
    run()
