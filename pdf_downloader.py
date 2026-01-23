import arxiv
import os

PDF_FOLDER = "pdfs"

def download_pdfs_by_topic(topic, max_papers=3):
    os.makedirs(PDF_FOLDER, exist_ok=True)

    search = arxiv.Search(
        query=topic,
        max_results=max_papers,
        sort_by=arxiv.SortCriterion.Relevance
    )

    downloaded = []

    for result in search.results():
        pdf_path = result.download_pdf(dirpath=PDF_FOLDER)
        downloaded.append(pdf_path)
        print(f"⬇ Downloaded: {os.path.basename(pdf_path)}")

    return downloaded
