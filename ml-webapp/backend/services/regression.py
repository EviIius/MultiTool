import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

async def train_regression(ws, X: pd.DataFrame, y: pd.Series, hp: dict):
    n_est      = hp.get("n_estimators", 100)
    max_depth  = hp.get("max_depth", None)
    criterion  = hp.get("criterion", "squared_error")

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2)
    model = RandomForestRegressor(
        warm_start=True,
        n_estimators=1,
        max_depth=max_depth,
        criterion=criterion
    )

    for i in range(1, n_est + 1):
        model.set_params(n_estimators=i)
        model.fit(X_tr, y_tr)
        await ws.send_json({"progress": round(100 * i / n_est, 1)})

    preds = model.predict(X_te)
    res = {
        "mse": mean_squared_error(y_te, preds),
        "actual": y_te.tolist(),
        "predicted": preds.tolist()
    }
    return res
