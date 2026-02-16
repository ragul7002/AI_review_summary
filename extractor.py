import fitz
import json
import os
import re

def first_n_sentences(text, n=3):
    s = re.split(r'(?<=[.!?]) +', text)
    return " ".join(s[:n])

def extract_with_layout(pdf_path, output_folder="extracted_text"):
    doc = fitz.open(pdf_path)

    if len(doc) > 20:
        return None

    full_text = []
    for page in doc:
        t = page.get_text("text")
        if t.strip():
            t = re.sub(r'arXiv:\S+', '', t)
            full_text.append(t)

    full_text = "\n".join(full_text)
    if not full_text.strip():
        return None

    def sec(p):
        m = re.search(p, full_text, re.I | re.S)
        return first_n_sentences(m.group(2)) if m else ""

    data = {
        "abstract": sec(r"(abstract)\s*(.*?)(introduction|methodology)"),
        "methodology": sec(r"(methodology|methods)\s*(.*?)(results|discussion)"),
        "results": sec(r"(results|experiments)\s*(.*?)(conclusion)"),
        "conclusion": sec(r"(conclusion)\s*(.*?)(references)")
    }

    os.makedirs(output_folder, exist_ok=True)
    name = os.path.splitext(os.path.basename(pdf_path))[0]
    out = os.path.join(output_folder, name + ".json")

    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return out
