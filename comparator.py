import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_most_similar(json_files):
    texts = []
    names = []

    for p in json_files:
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
            texts.append(" ".join(d.values()))
            names.append(p)

    tfidf = TfidfVectorizer(stop_words="english", max_features=3000).fit_transform(texts)
    sim = cosine_similarity(tfidf)

    scores = sim[0]
    best_idx = scores[1:].argmax() + 1
    best_score = round(scores[best_idx], 3)

    print("\n📊 Cosine Similarity Scores:")
    for i, s in enumerate(scores):
        print(f"{names[0]} vs {names[i]} = {round(s,3)}")

    return names[best_idx], best_score
