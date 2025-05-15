

from typing import List, Tuple
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, LinearRegression

def train_classifier(texts: List[str], labels: List) -> Tuple[TfidfVectorizer, LogisticRegression]:
    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(texts)
    clf = LogisticRegression(max_iter=1000, random_state=42).fit(X, labels)
    return vec, clf

def predict_classifier(vec: TfidfVectorizer, clf: LogisticRegression, texts: List[str]):
    X = vec.transform(texts)
    return clf.predict(X).tolist()

def train_regressor(texts: List[str], targets: List[float]) -> Tuple[TfidfVectorizer, LinearRegression]:
    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(texts)
    reg = LinearRegression().fit(X, targets)
    return vec, reg

def predict_regressor(vec: TfidfVectorizer, reg: LinearRegression, texts: List[str]):
    X = vec.transform(texts)
    return reg.predict(X).tolist()
