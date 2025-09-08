import sqlite3
import time
import feedparser
from config import DB_PATH, RSS_FEEDS

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guid TEXT UNIQUE,
            title TEXT,
            summary TEXT,
            link TEXT,
            source TEXT,
            published TEXT,
            fetched_at INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT)
    ''')
    conn.commit()
    conn.close()

def save_article(item, source):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    guid = item.get('id') or item.get('link') or item.get('title')
    title = item.get('title','').strip()
    summary = item.get('summary','').strip()
    link = item.get('link','')
    published = item.get('published','')
    try:
        c.execute('''
            INSERT INTO articles (guid, title, summary, link, source, published, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (guid, title, summary, link, source, published, int(time.time())))
        conn.commit()
        inserted = True
    except sqlite3.IntegrityError:
        inserted = False
    conn.close()
    return inserted

def fetch_feeds():
    init_db()
    new_count = 0
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        source = feed.feed.get('title', feed_url)
        for entry in feed.entries:
            if save_article(entry, source):
                new_count += 1
    return new_count

def get_latest(limit=50):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM articles ORDER BY fetched_at DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_article_by_id(aid):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM articles WHERE id=?", (aid,))
    row = c.fetchone()
    conn.close()
    return row