"""Eje 1: embeddings × (SVM, Bagging, AdaBoost, RandomForest)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.classify import modelos
from src.data import load_dataset
from src.embeddings import a_densa, disponibles, construir
from src.evaluate import guardar_tabla, metricas_clasificacion
from src.plots import barras_f1


def run(incluir_sbert: bool = True):
    train, test, positiva = load_dataset()
    print(f"\nEje 1 — train={len(train)}  test={len(test)}  positiva={positiva}")
    y_train = train["label"].tolist()
    y_test = test["label"].tolist()
    textos_train = train["text"].tolist()
    textos_test = test["text"].tolist()

    filas = []
    for nombre in disponibles(incluir_sbert=incluir_sbert):
        print(f"\n  embedding: {nombre}")
        emb = construir(nombre)
        emb.fit(textos_train)
        Xtr = a_densa(emb.transform(textos_train))
        Xte = a_densa(emb.transform(textos_test))
        for nom_modelo, clf in modelos().items():
            clf.fit(Xtr, y_train)
            pred = clf.predict(Xte)
            m = metricas_clasificacion(y_test, pred, positiva)
            filas.append({"embedding": nombre, "modelo": nom_modelo, **m})
            print(f"    {nom_modelo:13}  F1={m['f1']:.3f}  recall={m['recall']:.3f}  acc={m['accuracy']:.3f}")

    df = guardar_tabla(filas, "clasificacion")
    barras_f1(df)
    return df


if __name__ == "__main__":
    run()
