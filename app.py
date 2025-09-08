from flask import Flask, render_template, g, redirect, url_for
from aggregator import init_db, fetch_feeds, get_latest, get_article_by_id
from telegram_post import run_posting_cycle
from apscheduler.schedulers.background import BackgroundScheduler
from config import FETCH_INTERVAL_MINUTES

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    articles = get_latest(50)
    return render_template("index.html", articles=articles)

@app.route("/article/<int:aid>")
def article(aid):
    a = get_article_by_id(aid)
    if not a:
        return redirect(url_for('index'))
    return render_template("article.html", a=a)

@app.route("/fetch-now")
def fetch_now():
    n = fetch_feeds()
    return f"Fetched {n} new articles."

@app.route("/post-now")
def post_now():
    p = run_posting_cycle()
    return f"Posted {p} articles to Telegram."

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_feeds, 'interval', minutes=FETCH_INTERVAL_MINUTES)
scheduler.add_job(run_posting_cycle, 'interval', minutes=max(6, FETCH_INTERVAL_MINUTES+1))
scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)