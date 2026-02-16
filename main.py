from pdf_downloader import download_pdfs_by_topic
from extractor import extract_with_layout
from comparator import find_most_similar
from draft_generator import generate_full_draft
from apa_formatter import format_apa_reference
import json, os

topic = input("Enter research topic: ").strip()

pdfs = download_pdfs_by_topic(topic)

extracted = []
for p in pdfs:
    j = extract_with_layout(p)
    if j:
        extracted.append(j)

best_json, cosine_score = find_most_similar(extracted)

draft = generate_full_draft([best_json])

apa = format_apa_reference(
    title=os.path.basename(best_json).replace(".json",""),
    year="2024",
    url="https://arxiv.org"
)

out = {
    "cosine_similarity_score": cosine_score,
    "draft": draft,
    "reference": apa
}

with open("final_output.json","w",encoding="utf-8") as f:
    json.dump(out,f,indent=2,ensure_ascii=False)

print("✅ Done. Output saved.")
