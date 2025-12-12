from typing import Optional, Tuple, Dict, Any
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


# TODO: Add logging and tracking functionality (MLFlow?)
# TODO: Add data retrieval from a file function _get_data() -> np.ndarray

# TODO: Add metrics for precision, recall
def _evaluate_classifier(model, X_val, y_val) -> Dict[str, float]:
    preds = model.predict(X_val)
    return {
        "accuracy": float(accuracy_score(y_val, preds)),
        "f1_macro": float(f1_score(y_val, preds, average="macro"))
    }


def logistic_regression(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: Optional[np.ndarray] = None,
    y_val: Optional[np.ndarray] = None,
    penalty: str = "l2",
    C: float = 1.0,
    max_iter: int = 1000
) -> Tuple[Any, Dict[str, float]]:
    model = LogisticRegression(
        penalty=penalty,
        C=C,
        max_iter=max_iter
    )
    model.fit(X_train, y_train)

    metrics = {}
    if X_val is not None and y_val is not None:
        metrics = _evaluate_classifier(model, X_val, y_val)

    return model, metrics


def random_forest_classifier(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: Optional[np.ndarray] = None,
    y_val: Optional[np.ndarray] = None,
    n_estimators: int = 100,
    max_depth: Optional[int] = None,
    random_state: int = 42
) -> Tuple[Any, Dict[str, float]]:
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state
    )
    model.fit(X_train, y_train)

    metrics = {}
    if X_val is not None and y_val is not None:
        metrics = _evaluate_classifier(model, X_val, y_val)

    return model, metrics


def xgb_classifier(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: Optional[np.ndarray] = None,
    y_val: Optional[np.ndarray] = None,
    n_estimators: int = 300,
    learning_rate: float = 0.05,
    max_depth: int = 6,
    subsample: float = 0.8,
    colsample_bytree: float = 0.8,
    random_state: int = 42
) -> Tuple[Any, Dict[str, float]]:
    model = XGBClassifier(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
        subsample=subsample,
        colsample_bytree=colsample_bytree,
        random_state=random_state,
        eval_metric="logloss"
    )
    model.fit(X_train, y_train)

    metrics = {}
    if X_val is not None and y_val is not None:
        metrics = _evaluate_classifier(model, X_val, y_val)

    return model, metrics


def svc(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: Optional[np.ndarray] = None,
    y_val: Optional[np.ndarray] = None,
    kernel: str = "rbf",
    C: float = 1.0,
    gamma: str = "scale"
) -> Tuple[Any, Dict[str, float]]:
    model = SVC(kernel=kernel, C=C, gamma=gamma)
    model.fit(X_train, y_train)

    metrics = {}
    if X_val is not None and y_val is not None:
        metrics = _evaluate_classifier(model, X_val, y_val)

    return model, metrics


def kneighbors_classifier(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: Optional[np.ndarray] = None,
    y_val: Optional[np.ndarray] = None,
    n_neighbors: int = 5,
    weights: str = "uniform"
) -> Tuple[Any, Dict[str, float]]:
    model = KNeighborsClassifier(
        n_neighbors=n_neighbors,
        weights=weights
    )
    model.fit(X_train, y_train)

    metrics = {}
    if X_val is not None and y_val is not None:
        metrics = _evaluate_classifier(model, X_val, y_val)

    return model, metrics


if __name__=="__main__":
    pass
    # data = _get_data() -> np.ndarray
    # X = data[:][:-1]
    # y = data[:][-1]
    # X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
    # logistic_regression(X_train, y_train, X_val, y_val)
    # random_forest_classifier(X_train, y_train, X_val, y_val)
    # xgb_classifier(X_train, y_train, X_val, y_val)
    # svc(X_train, y_train, X_val, y_val)
    # kneighbors_classifier(X_train, y_train, X_val, y_val)