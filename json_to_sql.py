import sqlite3
import json

conn = sqlite3.connect("research.db")
cur = conn.cursor()

with open("AI_fetch.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

for p in papers:
    cur.execute("""
        INSERT OR IGNORE INTO papers
        (paper_id, title, year, url, abstract)
        VALUES (?, ?, ?, ?, ?)
    """, (
        p["paperId"],
        p["title"],
        p["year"],
        p["url"],
        p["abstract"]
    ))

    for a in p["authors"]:
        cur.execute("""
            INSERT OR IGNORE INTO authors
            (author_id, author_name)
            VALUES (?, ?)
        """, (
            a["authorId"],
            a["name"]
        ))

        cur.execute("""
            INSERT OR IGNORE INTO paper_authors
            (paper_id, author_id)
            VALUES (?, ?)
        """, (
            p["paperId"],
            a["authorId"]
        ))

conn.commit()
conn.close()
print("JSON data inserted into SQL tables")
