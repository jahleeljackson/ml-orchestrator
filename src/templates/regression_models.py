from typing import Optional, Tuple, Dict, Any
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor


# TODO: Add logging and tracking functionality (MLFlow?)
# TODO: Add data retrieval from a file function _get_data() -> np.ndarray


# TODO: Add metrics for mae and mse
def _evaluate_regression(model, X_val, y_val) -> Dict[str, float]:
    preds = model.predict(X_val)
    return {
        "rmse": float(mean_squared_error(y_val, preds, squared=False)),
        "r2": float(r2_score(y_val, preds))
    }


def linear_regression(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: Optional[np.ndarray] = None,
    y_val: Optional[np.ndarray] = None,
    fit_intercept: bool = True
) -> Tuple[Any, Dict[str, float]]:
    model = LinearRegression(fit_intercept=fit_intercept)
    model.fit(X_train, y_train)

    metrics = {}
    if X_val is not None and y_val is not None:
        metrics = _evaluate_regression(model, X_val, y_val)

    return model, metrics


def random_forest_regressor(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: Optional[np.ndarray] = None,
    y_val: Optional[np.ndarray] = None,
    n_estimators: int = 100,
    max_depth: Optional[int] = None,
    random_state: int = 42
) -> Tuple[Any, Dict[str, float]]:
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state
    )
    model.fit(X_train, y_train)

    metrics = {}
    if X_val is not None and y_val is not None:
        metrics = _evaluate_regression(model, X_val, y_val)

    return model, metrics


def xgb_regressor(
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
    model = XGBRegressor(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
        subsample=subsample,
        colsample_bytree=colsample_bytree,
        random_state=random_state,
        objective="reg:squarederror"
    )
    model.fit(X_train, y_train)

    metrics = {}
    if X_val is not None and y_val is not None:
        metrics = _evaluate_regression(model, X_val, y_val)

    return model, metrics


def svr(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: Optional[np.ndarray] = None,
    y_val: Optional[np.ndarray] = None,
    kernel: str = "rbf",
    C: float = 1.0,
    epsilon: float = 0.1
) -> Tuple[Any, Dict[str, float]]:
    model = SVR(kernel=kernel, C=C, epsilon=epsilon)
    model.fit(X_train, y_train)

    metrics = {}
    if X_val is not None and y_val is not None:
        metrics = _evaluate_regression(model, X_val, y_val)

    return model, metrics



if __name__=="__main__":
    pass
    # data = _get_data() -> np.ndarray
    # X = data[:][:-1]
    # y = data[:][-1]
    # X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
    # linear_regression(X_train, y_train, X_val, y_val)
    # random_forest_regressor(X_train, y_train, X_val, y_val)
    # xgb_regressor(X_train, y_train, X_val, y_val)
    # svr(X_train, y_train, X_val, y_val)