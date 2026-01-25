import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_most_similar(json_files):
    titles = []
    texts = []

    for path in json_files:
        if path is None:
            continue

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        text = data.get("full_text", "").strip()

        if text:
            titles.append(path.split("\\")[-1].replace(".json", ""))
            texts.append(text)

    if len(texts) < 2:
        print("❌ Not enough usable papers (RAW text missing)")
        return

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )
    tfidf = vectorizer.fit_transform(texts)

    similarity_matrix = cosine_similarity(tfidf)

    base_paper = titles[0]
    scores = similarity_matrix[0]

    similarities = sorted(
        list(enumerate(scores)),
        key=lambda x: x[1],
        reverse=True
    )

    best_match_index, best_score = similarities[1]

    print("📄 Paper:")
    print(base_paper)

    print("\n🔍 Most similar to:")
    print(titles[best_match_index])

    print("\n📊 Similarity score:")
    print(round(best_score, 2))
