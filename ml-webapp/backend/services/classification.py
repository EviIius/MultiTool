import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_curve

async def train_classification(ws, X: pd.DataFrame, y: pd.Series, hp: dict):
    n_est      = hp.get("n_estimators", 100)
    max_depth  = hp.get("max_depth", None)
    criterion  = hp.get("criterion", "gini")

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier(
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
    res = {"accuracy": accuracy_score(y_te, preds)}

    # ROC if binary
    try:
        probs = model.predict_proba(X_te)[:, 1]
        if len(set(y_te)) == 2:
            fpr, tpr, _ = roc_curve(y_te, probs)
            res.update({"fpr": fpr.tolist(), "tpr": tpr.tolist()})
    except:
        pass

    return res
