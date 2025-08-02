import os
from dotenv import load_dotenv

load_dotenv()  # .env faylını oxu

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID")) if os.getenv("ADMIN_ID") else None
CARD_NUMBER = os.getenv("CARD_NUMBER") or "4098 5844 6547 4300"
DB_PATH = os.getenv("DB_PATH") or "database.db"

if not BOT_TOKEN or not ADMIN_ID:
    raise ValueError("BOT_TOKEN və ADMIN_ID .env faylında təyin olunmalıdır.")