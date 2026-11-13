# deteccion-phishing

Clasificar correos de phishing y explicar la decisión con un RAG.

El eje 1 dice si el correo es phishing o ham. Compara TF-IDF, CBOW, Skip-gram y GloVe con SVM, bagging, AdaBoost y random forest.

El eje 2 no vuelve a etiquetar. Busca 3 fragmentos en una base de 7 reglas y 6 campañas (están en `src/corpus.py`) y Gemma 2B escribe el porqué citando esos IDs. Gemma corre en local, por Ollama (`localhost:11434`). Si Ollama no está, se pegan los fragmentos (modo extractivo). No busca en internet.

Hay 64 correos en español en `src/corpus.py`: 48 de train y 16 de test. Al correr se copian a `data/`.

## Cómo correrlo

Desde esta carpeta:

```bash
python3 -m pip install -r requirements.txt
```

Para Gemma (eje 2 y demo):

```bash
ollama serve
ollama pull gemma2:2b
```

```bash
python3 run.py demo     # un correo (p25): SVM+TF-IDF, luego Gemma con RAG y sin RAG
python3 run.py eje1     # tabla de clasificación
python3 run.py eje2     # retrievers (Recall@3 y MRR) y un recorrido del RAG
python3 run.py          # los tres, en ese orden
```

`--llm` por defecto es `auto`: usa Ollama si responde en `/api/tags`; si no, extractivo.

```bash
python3 run.py demo --llm extractivo
python3 run.py demo --llm ollama --model gemma2:2b
python3 run.py eje2 --k 3
```

También se puede entrar por el script:

```bash
python3 experiments/demo.py
python3 experiments/eje1.py
python3 experiments/eje2.py
```

URLs y modelo de Ollama: `src/config.py` (`OLLAMA_URL`, `OLLAMA_TAGS`, `OLLAMA_MODEL`). La llamada HTTP está en `src/rag.py`.

## Carpetas

```
run.py
requirements.txt
src/
  corpus.py       correos, reglas, campañas, preguntas
  config.py       rutas, semilla, TOP_K=3, Ollama
  embeddings.py   tfidf, cbow, skipgram, glove
  classify.py     SVM, bagging, AdaBoost, random forest
  rag.py          BM25, índices, prompt, Ollama
  evaluate.py     F1, recall, Recall@k, MRR
experiments/
  demo.py
  eje1.py
  eje2.py
  results/        se crea al correr
data/             CSV/JSON copiados desde corpus.py
outputs/          gráficos (eje 1 y eje 2)
```

## Qué sale al correr

| Archivo | De dónde |
|---|---|
| `experiments/results/demo.md` | `run.py demo` |
| `experiments/results/clasificacion.csv` | `run.py eje1` — accuracy, precision, recall, F1 |
| `outputs/f1_clasificacion.png` | `run.py eje1` |
| `experiments/results/rag_retrieval.csv` | `run.py eje2` — Recall@k y MRR |
| `experiments/results/rag_recorrido.md` | `run.py eje2` — prompt y respuesta |
| `experiments/results/rag_ejemplos.json` | `run.py eje2` |
| `outputs/rag_recall.png` | `run.py eje2` |

En el eje 2 el retriever puede ser BM25, TF-IDF (coseno), CBOW, Skip-gram o GloVe. BM25 está en `src/rag.py`; Recall@3 y MRR se calculan en `src/evaluate.py` sobre las 8 preguntas de `PREGUNTAS` en `src/corpus.py`. Cada pregunta tiene `gold_chunk_ids`. El índice usa solo reglas y campañas (`incluir_correos_train=False` en `experiments/eje2.py`).

`sentence-transformers` no está en `requirements.txt`. Si lo instalas, entra también `sbert`. Si no, se omite. Para no usarlo: `python3 run.py --no-sbert`.
