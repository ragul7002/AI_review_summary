import os
import json
import re
from collections import Counter

DATA_FOLDER = "extracted_text"

# ---------------- TEXT CLEANING ----------------
def clean_text(text):
    if not text:
        return ""

    text = text.replace("-\n", "")          # fix broken words
    text = text.replace("\n", " ")           # remove new lines
    text = re.sub(r"(?<=\w)(?=[A-Z])", " ", text)  # split joined words
    text = re.sub(r"\s+", " ", text)         # remove extra spaces
    return text.strip()

# ---------------- KEY FINDINGS ----------------
def extract_key_findings(text, top_n=5):
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 40]

    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    freq = Counter(words)

    scored = []
    for s in sentences:
        score = sum(freq[w] for w in re.findall(r"\b[a-zA-Z]+\b", s.lower()))
        scored.append((score, s))

    scored.sort(reverse=True)
    return [s for _, s in scored[:top_n]]

# ---------------- MAIN PROCESS ----------------
all_abstracts = []

for file in os.listdir(DATA_FOLDER):
    if not file.endswith(".json"):
        continue

    with open(os.path.join(DATA_FOLDER, file), "r", encoding="utf-8") as f:
        data = json.load(f)

    abstract = clean_text(data.get("abstract", ""))
    conclusion = clean_text(data.get("conclusion", ""))

    combined_text = abstract + " " + conclusion
    findings = extract_key_findings(combined_text)

    print(f"\n📄 Paper: {file}")
    if findings:
        for f in findings:
            print("•", f)
    else:
        print("• No significant findings extracted")

    if abstract:
        all_abstracts.append(abstract)

# ---------------- CROSS PAPER COMPARISON ----------------
if len(all_abstracts) > 1:
    common_words = set(re.findall(r"\b[a-zA-Z]+\b", all_abstracts[0].lower()))

    for text in all_abstracts[1:]:
        words = set(re.findall(r"\b[a-zA-Z]+\b", text.lower()))
        common_words &= words

    # remove useless words
    stopwords = {
        "the","and","to","of","in","for","a","is","on","with",
        "that","as","are","this","be","by","an"
    }

    common_words = [w for w in common_words if w not in stopwords]

    print("\n🔗 Common concepts across papers:")
    print(common_words[:20])
else:
    print("\n⚠️ Not enough papers for cross-paper comparison")
