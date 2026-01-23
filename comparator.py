import os
import json
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

EXTRACTED_FOLDER = "extracted_text"

# ----- clean text -----
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    return text

# ----- load JSON files -----
def load_papers():
    papers = {}
    for file in os.listdir(EXTRACTED_FOLDER):
        if file.endswith(".json"):
            path = os.path.join(EXTRACTED_FOLDER, file)
            with open(path, encoding="utf-8") as f:
                papers[file] = json.load(f)
    return papers

# ----- abstracts -----
def compare_abstracts():
    papers = load_papers()
    abstracts = {}
    for name, data in papers.items():
        abstracts[name] = data.get("abstract", "")
    return abstracts

# ----- keyword overlap -----
def keyword_overlap(top_n=10):
    papers = load_papers()
    keyword_map = {}
    for name, data in papers.items():
        text = data.get("abstract", "")
        cleaned = clean_text(text)
        words = cleaned.split()
        common = Counter(words).most_common(top_n)
        keyword_map[name] = common
    return keyword_map

# ----- TF-IDF + Cosine similarity -----
def compute_similarity():
    abstracts = compare_abstracts()
    names = list(abstracts.keys())
    texts = list(abstracts.values())

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)

    sim_matrix = cosine_similarity(tfidf_matrix)

    similarity_scores = {}
    for i, name in enumerate(names):
        similarity_scores[name] = {}
        for j, other_name in enumerate(names):
            similarity_scores[name][other_name] = round(sim_matrix[i][j], 3)
    return similarity_scores

# ----- Most similar paper per PDF -----
def most_similar_papers():
    sim_scores = compute_similarity()
    top_sim = {}

    for paper, sims in sim_scores.items():
        sims_filtered = {k: v for k, v in sims.items() if k != paper}
        if not sims_filtered:
            continue
        most_similar = max(sims_filtered, key=lambda x: sims_filtered[x])
        top_sim[paper] = (most_similar, sims_filtered[most_similar])
    return top_sim
