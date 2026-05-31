# 🎬 YouTube Downloader Telegram Bot

YouTube videolarini turli format va sifatlarda yuklab olish imkonini beruvchi Telegram bot.

## ✨ Imkoniyatlar

- 🎥 **Video formatlar**: MP4, WebM
- 🎵 **Audio formatlar**: MP3, M4A
- 📱 **Video sifatlar**: 360p, 480p, 720p, 1080p
- 🔊 **Audio sifatlar**: 128kbps, 192kbps, 320kbps
- ⚡ Tez va qulay interfeys
- 🔘 Inline tugmalar orqali boshqarish

## 🚀 O'rnatish

### 1. Repozitoriyani klonlash

```bash
git clone https://github.com/zoirj84-cpu/men-uchun.git
cd men-uchun
```

### 2. Virtual muhit yaratish

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. FFmpeg o'rnatish

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg -y
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
[FFmpeg rasmiy saytidan](https://ffmpeg.org/download.html) yuklab oling.

### 5. Bot tokenini sozlash

```bash
cp .env.example .env
```

`.env` faylini oching va `BOT_TOKEN` ni [BotFather](https://t.me/BotFather) dan olingan token bilan almashtiring:

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 6. Botni ishga tushirish

```bash
python bot.py
```

## 📁 Loyiha strukturasi

```
men-uchun/
├── bot.py           # Asosiy bot fayli
├── downloader.py    # YouTube yuklab olish moduli
├── config.py        # Konfiguratsiya
├── requirements.txt # Kutubxonalar
├── .env.example     # Muhit o'zgaruvchilari namunasi
├── .gitignore       # Git ignore
└── README.md        # Hujjat
```

## 🤖 Foydalanish

1. Botni Telegram'da toping va `/start` yuboring
2. YouTube video havolasini yuboring
3. Format tanlang (MP4 / MP3 / WebM / M4A)
4. Sifat tanlang
5. Fayl avtomatik yuboriladi!

## ⚙️ Buyruqlar

| Buyruq | Tavsif |
|--------|--------|
| `/start` | Botni boshlash |
| `/help` | Yordam |
| `/about` | Bot haqida |

## 📋 Talablar

- Python 3.10+
- FFmpeg
- Telegram Bot Token

## ⚠️ Muhim eslatmalar

- Telegram 50MB dan katta fayllarni qabul qilmaydi
- Faqat ommaviy videolar uchun ishlaydi
- Mualliflik huquqiga rioya qiling

## 🛠 Texnologiyalar

- [python-telegram-bot](https://python-telegram-bot.org/) v20.7
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube yuklab olish
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Muhit o'zgaruvchilari

## 📜 Litsenziya

MIT License
