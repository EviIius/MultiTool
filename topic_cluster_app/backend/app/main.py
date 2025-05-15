

import os, io
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import pandas as pd

from .clustering import *
from .reduce       import *
from .supervised   import *
from .nlp          import *

app = FastAPI(title="Multi-Method Text Analytics")

def get_texts(raw: bytes) -> List[str]:
    return raw.decode("utf-8").splitlines()

# — Unsupervised clustering endpoints —

@app.post("/kmeans/")
async def api_kmeans(file: UploadFile = File(...), n_clusters: int = Form(...)):
    texts = get_texts(await file.read())
    labels, top_terms = kmeans_cluster(texts, n_clusters)
    return {"labels": labels, "top_terms": top_terms}

@app.post("/lda/")
async def api_lda(file: UploadFile = File(...), n_topics: int = Form(...)):
    texts = get_texts(await file.read())
    doc_topics, topics = lda_topics(texts, n_topics)
    return {"doc_topics": doc_topics, "topics": topics}

@app.post("/hierarchy/")
async def api_hierarchy(file: UploadFile = File(...), n_clusters: int = Form(...)):
    texts = get_texts(await file.read())
    return {"labels": hier_cluster(texts, n_clusters)}

@app.post("/dbscan/")
async def api_dbscan(
    file: UploadFile = File(...),
    eps: float = Form(0.5),
    min_samples: int = Form(5)
):
    texts = get_texts(await file.read())
    return {"labels": dbscan_cluster(texts, eps, min_samples)}

@app.post("/hdbscan/")
async def api_hdbscan(file: UploadFile = File(...), min_cluster_size: int = Form(5)):
    texts = get_texts(await file.read())
    return {"labels": hdbscan_cluster(texts, min_cluster_size)}

@app.post("/anomaly/")
async def api_anomaly(file: UploadFile = File(...)):
    texts = get_texts(await file.read())
    return {"labels": anomaly_detect(texts)}

# — Dimensionality reduction endpoints —

@app.post("/pca/")
async def api_pca(file: UploadFile = File(...), n_components: int = Form(2)):
    texts = get_texts(await file.read())
    return {"coords": pca_reduce(texts, n_components)}

@app.post("/tsne/")
async def api_tsne(
    file: UploadFile = File(...),
    n_components: int = Form(2),
    perplexity: float = Form(30.0)
):
    texts = get_texts(await file.read())
    return {"coords": tsne_reduce(texts, n_components, perplexity)}

@app.post("/umap/")
async def api_umap(file: UploadFile = File(...), n_components: int = Form(2)):
    texts = get_texts(await file.read())
    return {"coords": umap_reduce(texts, n_components)}

# — Supervised learning endpoints —

@app.post("/classify/")
async def api_classify(
    train_file: UploadFile = File(...),
    text_col: str          = Form("text"),
    label_col: str         = Form("label"),
    predict_file: UploadFile = File(None)
):
    raw = await train_file.read()
    df  = pd.read_csv(io.StringIO(raw.decode("utf-8")))
    if text_col not in df or label_col not in df:
        raise HTTPException(400, "CSV must have those columns")
    vec, clf = train_classifier(df[text_col].tolist(), df[label_col].tolist())
    if predict_file:
        texts = get_texts(await predict_file.read())
        return {"predictions": predict_classifier(vec, clf, texts)}
    return {"detail": "Model trained. POST a predict_file to get predictions."}

@app.post("/regress/")
async def api_regress(
    train_file: UploadFile = File(...),
    text_col: str          = Form("text"),
    target_col: str        = Form("target"),
    predict_file: UploadFile = File(None)
):
    raw = await train_file.read()
    df  = pd.read_csv(io.StringIO(raw.decode("utf-8")))
    if text_col not in df or target_col not in df:
        raise HTTPException(400, "CSV must have those columns")
    vec, reg = train_regressor(df[text_col].tolist(), df[target_col].tolist())
    if predict_file:
        texts = get_texts(await predict_file.read())
        return {"predictions": predict_regressor(vec, reg, texts)}
    return {"detail": "Model trained. POST a predict_file to get predictions."}

# — Embedding, summarization, sentiment & NER —

@app.post("/embed_cluster/")
async def api_embed_cluster(file: UploadFile = File(...), n_clusters: int = Form(...)):
    texts = get_texts(await file.read())
    return {"labels": embed_clustering(texts, n_clusters)}

@app.post("/summarize/")
async def api_summarize(file: UploadFile = File(...), max_length: int = Form(50)):
    texts    = get_texts(await file.read())
    summary  = summarize_texts(texts, max_length)
    return {"summaries": summary}

@app.post("/sentiment/")
async def api_sentiment(file: UploadFile = File(...)):
    texts   = get_texts(await file.read())
    results = sentiment_texts(texts)
    return {"sentiment": results}

@app.post("/ner/")
async def api_ner(file: UploadFile = File(...)):
    texts   = get_texts(await file.read())
    ents    = ner_texts(texts)
    return {"entities": ents}

# — Serve your SPA —

@app.get("/", response_class=HTMLResponse)
async def read_index():
    here = os.path.dirname(__file__)
    path = os.path.join(here, "..", "static", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
