import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db.sqlite")

# روابط RSS الرسمية أو المعدّة
RSS_FEEDS = [
    "https://www.marca.com/rss/en/all.xml",
    "https://as.com/rss/portada.xml"
]

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")  # مثال: @yourchannel أو -1001234567890

# إعدادات الجلب
FETCH_INTERVAL_MINUTES = int(os.getenv("FETCH_INTERVAL_MINUTES", "5"))