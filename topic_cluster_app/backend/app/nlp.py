from typing import List
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import spacy

# load heavy models once at import time
embed_model      = SentenceTransformer("all-MiniLM-L6-v2")
summarizer      = pipeline("summarization")
sentiment_pipe  = pipeline("sentiment-analysis")
nlp_spacy       = spacy.load("en_core_web_sm")

def embed_clustering(texts: List[str], n_clusters: int):
    from sklearn.cluster import KMeans
    X = embed_model.encode(texts, convert_to_numpy=True)
    model = KMeans(n_clusters=n_clusters, random_state=42).fit(X)
    return model.labels_.tolist()

def summarize_texts(texts: List[str], max_length: int = 50):
    return [s["summary_text"] for s in summarizer(texts, max_length=max_length)]

def sentiment_texts(texts: List[str]):
    return sentiment_pipe(texts)

def ner_texts(texts: List[str]):
    results = []
    for doc in nlp_spacy.pipe(texts):
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        results.append(entities)
    return results
