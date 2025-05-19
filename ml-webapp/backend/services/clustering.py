import pandas as pd
from sklearn.cluster import KMeans

async def train_clustering(ws, X: pd.DataFrame, hp: dict):
    n_clusters = hp.get("n_clusters", 3)
    init       = hp.get("init", "k-means++")
    max_iter   = hp.get("max_iter", 300)

    km = KMeans(n_clusters=n_clusters, init=init, max_iter=max_iter)
    labels = km.fit_predict(X)

    # Scatter data on first two features
    data = [
        {"x": float(pt[0]), "y": float(pt[1]), "cluster": int(lbl)}
        for pt, lbl in zip(X.iloc[:, :2].values, labels)
    ]
    centers = [
        {"x": float(c[0]), "y": float(c[1]), "cluster": idx}
        for idx, c in enumerate(km.cluster_centers_[:, :2])
    ]

    await ws.send_json({"progress": 100})
    return {"labels": labels.tolist(), "data": data, "centers": centers}
