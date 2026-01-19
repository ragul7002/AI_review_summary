import os
import requests
import xml.etree.ElementTree as ET
import pdfplumber
import re
import json
import sys

PDF_FOLDER = "pdfs"
OUTPUT_FOLDER = "extracted_text"

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

STOP_SECTIONS = [
    "references",
    "acknowledgment",
    "acknowledgement",
    "appendix"
]

# ---------------- TEXT EXTRACTION ----------------

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# ---------------- ABSTRACT CLEANER ----------------

def extract_clean_abstract(text):
    lower = text.lower()

    matches = list(re.finditer(r"\babstract\b", lower))
    if not matches:
        return None

    for m in matches:
        start = m.end()
        end = len(text)

        intro = re.search(r"\bintroduction\b", lower[start:])
        if intro:
            end = start + intro.start()

        candidate = text[start:end]
        candidate = re.sub(r"\n+", " ", candidate)
        candidate = re.sub(r"\s+", " ", candidate).strip()

        # ❌ Reject noise
        reject_words = [
            "keywords",
            "reference",
            "table",
            "figure",
            "acknowledg",
            "appendix",
            "copyright"
        ]

        if any(r in candidate.lower() for r in reject_words):
            continue

        words = candidate.split()
        if 80 <= len(words) <= 300:
            return candidate

    return None


# ---------------- SECTION EXTRACTION ----------------

def extract_sections(text):
    data = {}
    lower = text.lower()

    abstract = extract_clean_abstract(text)
    if abstract:
        data["abstract"] = abstract

    sections = [
        "introduction",
        "methods",
        "methodology",
        "results",
        "discussion",
        "conclusion"
    ]

    for sec in sections:
        match = re.search(rf"\b{sec}\b", lower)
        if not match:
            continue

        start = match.end()
        end = len(text)

        # stop at next section or stop-section
        for stopper in sections + STOP_SECTIONS:
            if stopper == sec:
                continue
            s = re.search(rf"\b{stopper}\b", lower[start:])
            if s:
                end = min(end, start + s.start())

        chunk = text[start:end]
        chunk = re.sub(r"\n+", " ", chunk)
        chunk = re.sub(r"\s+", " ", chunk).strip()

        if len(chunk.split()) > 100:
            data[sec] = chunk

    return data


# ---------------- PDF DOWNLOAD WITH PROGRESS BAR ----------------

def download_file(url, dest_folder):
    filename = url.split("/")[-1] + ".pdf"
    file_path = os.path.join(dest_folder, filename)

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    chunk_size = 1024  # 1 KB

    downloaded = 0
    with open(file_path, "wb") as f:
        for data in response.iter_content(chunk_size):
            f.write(data)
            downloaded += len(data)
            if total_size > 0:
                done = int(30 * downloaded / total_size)  # 30 chars progress bar
                percent = (downloaded / total_size) * 100
                sys.stdout.write(
                    f"\r⬇️ Downloading: {filename} "
                    f"[{'█' * done}{'░' * (30-done)}] "
                    f"{percent:.1f}% | {downloaded/1024/1024:.2f}MB/{total_size/1024/1024:.2f}MB"
                )
                sys.stdout.flush()

    sys.stdout.write("\n✅ Downloaded: " + filename + "\n")
    return file_path


# ---------------- arXiv SEARCH ----------------

topic = input("Enter research topic: ").strip()
num_papers = int(input("Number of papers (default 5): ") or 5)

url = f"http://export.arxiv.org/api/query?search_query=all:{topic}&start=0&max_results={num_papers}"
response = requests.get(url)
root = ET.fromstring(response.content)

ns = {'atom': 'http://www.w3.org/2005/Atom'}
pdf_links = []

for entry in root.findall('atom:entry', ns):
    pdf = entry.find("atom:link[@title='pdf']", ns)
    if pdf is not None:
        pdf_links.append(pdf.attrib['href'])

# ---------------- PROCESS ----------------

for pdf in pdf_links:
    pdf_path = download_file(pdf, PDF_FOLDER)

    text = extract_text(pdf_path)
    sections = extract_sections(text)

    if sections:
        out = os.path.join(OUTPUT_FOLDER, os.path.basename(pdf_path).replace(".pdf", ".json"))
        with open(out, "w", encoding="utf-8") as f:
            json.dump(sections, f, indent=2, ensure_ascii=False)
        print(f"✅ Clean sections saved: {out}\n")
    else:
        print(f"⚠ No valid sections: {os.path.basename(pdf_path)}\n")

print("✅CLEAN TEXT EXTRACTION DONE")
