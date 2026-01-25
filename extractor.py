import fitz  # PyMuPDF
import json
import os


def extract_with_layout(pdf_path, output_folder="extracted_text"):
    doc = fitz.open(pdf_path)

    full_text = []

    for page in doc:
        text = page.get_text("text")
        if text.strip():
            full_text.append(text)

    full_text = "\n".join(full_text)

    if not full_text.strip():
        print(f"⚠ No text found in {pdf_path}")
        return None

    os.makedirs(output_folder, exist_ok=True)
    base = os.path.basename(pdf_path).replace(".pdf", "")
    json_path = os.path.join(output_folder, f"{base}.json")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {"full_text": full_text[:15000]},  # limit size
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"✅ Extracted RAW TEXT: {json_path}")
    return json_path
