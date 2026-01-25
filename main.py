print("🔥 main.py started")

from pdf_downloader import download_pdfs_by_topic
from extractor import extract_with_layout
from comparator import find_most_similar


if __name__ == "__main__":

    topic = input("Enter research topic: ").strip()

    print("\n🔍 Downloading PDFs for topic:", topic)
    pdfs = download_pdfs_by_topic(topic, max_papers=3)

    print("\n📄 Extracting RAW text from PDFs...\n")
    extracted_jsons = []

    for pdf in pdfs:
        json_path = extract_with_layout(pdf)
        if json_path:
            extracted_jsons.append(json_path)

    if len(extracted_jsons) < 2:
        print("\n❌ Not enough usable PDFs after extraction")
    else:
        print("\n📊 FINDING MOST SIMILAR PAPER...\n")
        find_most_similar(extracted_jsons)

    print("\n✅ PROCESS COMPLETED")
