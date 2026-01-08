import requests
import time
import json

def fetch_papers(topic, limit=5, retries=3, wait_seconds=5):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {"query": topic, "limit": limit, "fields": "title,authors,year,abstract,url"}
    for attempt in range(retries):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        elif response.status_code == 429:
            print(f"Rate limit hit. Waiting {wait_seconds} seconds...")
            time.sleep(wait_seconds)
        else:
            response.raise_for_status()
    return []

def show_papers(papers):
    if not papers:
        print("No papers found.")
        return
    for i, paper in enumerate(papers, start=1):
        authors = ", ".join(a.get("name", "") for a in paper.get("authors", []))
        print(f"\nPaper {i}")
        print("Title:", paper.get("title", "N/A"))
        print("Authors:", authors or "N/A")
        print("Year:", paper.get("year", "N/A"))
        print("Abstract:", paper.get("abstract", "N/A"))
        print("URL:", paper.get("url", "N/A"))
        print("-" * 60)

def save_papers_json(papers, filename="AI_fetch.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(papers, file, indent=4, ensure_ascii=False)
    print(f"Dataset saved as {filename}")

if __name__ == "__main__":
    topic = "Machine Learning"
    print("Fetching papers...")
    papers = fetch_papers(topic)
    show_papers(papers)
    save_papers_json(papers)  # <<< Add this in AI_review.py
