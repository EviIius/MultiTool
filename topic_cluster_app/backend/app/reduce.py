from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap

def _vectorize(texts: List[str]):
    return TfidfVectorizer(stop_words="english").fit_transform(texts).toarray()

def pca_reduce(texts: List[str], n_components: int = 2):
    X = _vectorize(texts)
    coords = PCA(n_components=n_components, random_state=42).fit_transform(X)
    return coords.tolist()

def tsne_reduce(texts: List[str], n_components: int = 2, perplexity: float = 30.0):
    X = _vectorize(texts)
    coords = TSNE(n_components=n_components, perplexity=perplexity, random_state=42).fit_transform(X)
    return coords.tolist()

def umap_reduce(texts: List[str], n_components: int = 2):
    X = _vectorize(texts)
    coords = umap.UMAP(n_components=n_components, random_state=42).fit_transform(X)
    return coords.tolist()
