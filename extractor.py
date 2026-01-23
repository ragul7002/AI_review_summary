import pymupdf.layout   # MUST be first
import pymupdf4llm
import json
import os
import re
from PIL import Image
import pytesseract

# ----- set Tesseract path if needed -----
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

OUTPUT_FOLDER = "extracted_text"

# ----- detect section -----
def detect_section(line):
    text = line.lower().strip()
    patterns = {
        "abstract": r"\babstract\b",
        "introduction": r"\bintroduction\b",
        "methods": r"\b(methods?|methodology|materials and methods)\b",
        "results": r"\bresults?\b",
        "conclusion": r"\b(conclusion|conclusions|discussion|summary)\b"
    }
    for section, pattern in patterns.items():
        if re.search(pattern, text):
            return section
    return None

# ----- extract text + segment -----
def extract_with_layout(pdf_path, out_name=None):
    print(f"📄 Extracting: {os.path.basename(pdf_path)}")

    md_text = pymupdf4llm.to_markdown(
        pdf_path,
        page_chunks=False,
        margins=(10, 10, 10, 10)
    )

    sections = {}
    current_section = None

    for line in md_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        found_section = detect_section(stripped)
        if found_section:
            current_section = found_section
            sections.setdefault(current_section, [])
            continue

        if current_section:
            sections[current_section].append(line)

    for k in sections:
        sections[k] = "\n".join(sections[k]).strip()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # shorten filename
    if out_name:
        base = out_name.replace(".json","")
    else:
        base = os.path.basename(pdf_path).split(".")[0]

    out_file = os.path.join(OUTPUT_FOLDER, f"{base}.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved JSON: {out_file}")
    print("📌 Sections found:", list(sections.keys()))

    return sections
