import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# Bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi! .env faylini tekshiring.")

# Yuklab olish sozlamalari
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))  # Telegram limiti: 50MB
DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", "300"))  # 5 daqiqa

# Admin ID (ixtiyoriy)
ADMIN_ID = os.getenv("ADMIN_ID", None)
if ADMIN_ID:
    ADMIN_ID = int(ADMIN_ID)
