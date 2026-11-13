"""Clasificadores del eje 1: SVM, bagging, AdaBoost y random forest."""
from __future__ import annotations

from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier, RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

from src.config import RANDOM_STATE


def _ensamble(cls, tree, **kwargs):
    """Compatibilidad de sklearn: estimator o base_estimator."""
    try:
        return cls(estimator=tree, **kwargs)
    except TypeError:
        return cls(base_estimator=tree, **kwargs)


def modelos() -> dict:
    arbol = DecisionTreeClassifier(max_depth=6, random_state=RANDOM_STATE)
    arbol_prof1 = DecisionTreeClassifier(max_depth=1, random_state=RANDOM_STATE)
    return {
        "SVM": LinearSVC(class_weight="balanced", random_state=RANDOM_STATE, max_iter=4000),
        "Bagging": _ensamble(
            BaggingClassifier,
            arbol,
            n_estimators=40,
            max_samples=0.8,
            bootstrap=True,
            random_state=RANDOM_STATE,
        ),
        "AdaBoost": _ensamble(
            AdaBoostClassifier,
            arbol_prof1,
            n_estimators=40,
            random_state=RANDOM_STATE,
        ),
        "RandomForest": RandomForestClassifier(
            n_estimators=80,
            max_depth=8,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
    }
