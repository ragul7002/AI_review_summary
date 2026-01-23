print("🔥 main.py started")

from pdf_downloader import download_pdfs_by_topic
from extractor import extract_with_layout
from comparator import compare_abstracts, keyword_overlap, compute_similarity, most_similar_papers

if __name__ == "__main__":

    # ----- topic input -----
    topic = input("Enter research topic: ").strip()

    # ----- download PDFs -----
    print("\n🔍 Downloading PDFs for topic:", topic)
    pdfs = download_pdfs_by_topic(topic, max_papers=5)

    # ----- extract + segment -----
    print("\n📄 Extracting & segmenting PDFs...")
    for idx, pdf in enumerate(pdfs, start=1):
        # assign short name like Earth_1, Earth_2
        extract_with_layout(pdf, out_name=f"{topic}_{idx}.json")

    # ----- compare abstracts -----
    print("\n📊 COMPARING ABSTRACTS...\n")
    abstracts = compare_abstracts()
    for paper, text in abstracts.items():
        print("📝", paper)
        print(text[:500], "\n")  # first 500 chars

    # ----- keyword overlap -----
    print("\n🔑 KEYWORD OVERLAP (from abstracts)\n")
    keywords = keyword_overlap()
    for paper, words in keywords.items():
        print("📌", paper)
        print(words, "\n")

    # ----- cosine similarity -----
    print("\n📈 COMPUTING PAIRWISE SIMILARITY (TF-IDF + Cosine) ...\n")
    sim_matrix = compute_similarity()

    # neat descending display
    for paper, sims in sim_matrix.items():
        print(f"📝 {paper} (all similarities sorted)")
        sorted_sims = sorted(
            [(other, s) for other, s in sims.items() if other != paper],
            key=lambda x: x[1],
            reverse=True
        )
        for other, score in sorted_sims:
            print(f"   {other}: {score}")
        print()

    # ----- most similar paper per PDF -----
    print("\n🔥 MOST SIMILAR PAPER PER PDF 🔥\n")
    top_sim = most_similar_papers()
    for paper, (most_similar, score) in top_sim.items():
        print(f"📝 {paper}")
        print(f"   Most similar: {most_similar} | Score: {score}\n")

    print("✅ PIPELINE COMPLETE")
