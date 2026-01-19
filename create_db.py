import sqlite3

conn = sqlite3.connect("research.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS papers (
    paper_id TEXT PRIMARY KEY,
    title TEXT,
    year INTEGER,
    url TEXT,
    abstract TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS authors (
    author_id TEXT PRIMARY KEY,
    author_name TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS paper_authors (
    paper_id TEXT,
    author_id TEXT,
    PRIMARY KEY (paper_id, author_id),
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
)
""")

conn.commit()
conn.close()
print("Database & tables created successfully")
