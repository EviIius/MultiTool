# backend/app/clustering.py

from typing import List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from hdbscan import HDBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import LatentDirichletAllocation

def kmeans_cluster(texts: List[str], n_clusters: int):
    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(texts)
    model = KMeans(n_clusters=n_clusters, random_state=42).fit(X)
    labels = model.labels_.tolist()
    terms = vec.get_feature_names_out()
    centroids = model.cluster_centers_.argsort()[:, ::-1]
    top_terms = [[terms[i] for i in centroid[:5]] for centroid in centroids]
    return labels, top_terms

def lda_topics(texts: List[str], n_topics: int):
    vec = CountVectorizer(stop_words="english")
    X = vec.fit_transform(texts)
    model = LatentDirichletAllocation(n_components=n_topics, random_state=42).fit(X)
    topics = []
    terms = vec.get_feature_names_out()
    for comp in model.components_:
        top = np.argsort(comp)[::-1][:5]
        topics.append([terms[i] for i in top])
    doc_topic = model.transform(X).argmax(axis=1).tolist()
    return doc_topic, topics

def hier_cluster(texts: List[str], n_clusters: int):
    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(texts).toarray()
    model = AgglomerativeClustering(n_clusters=n_clusters).fit(X)
    return model.labels_.tolist()

def dbscan_cluster(texts: List[str], eps: float = 0.5, min_samples: int = 5):
    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(texts).toarray()
    labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(X).tolist()
    return labels

def hdbscan_cluster(texts: List[str], min_cluster_size: int = 5):
    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(texts).toarray()
    labels = HDBSCAN(min_cluster_size=min_cluster_size).fit_predict(X).tolist()
    return labels

def anomaly_detect(texts: List[str]):
    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(texts).toarray()
    iso = IsolationForest(random_state=42).fit(X)
    #  1 = normal, -1 = anomaly
    return iso.predict(X).tolist()
