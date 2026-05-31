import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from downloader import get_video_info, download_video, download_audio
from config import BOT_TOKEN

# Logging sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Foydalanuvchi holati
user_data_store = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Botni boshlash"""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Salom, {user.first_name}!\n\n"
        "🎬 Men YouTube videolarini yuklab olishga yordam beraman.\n\n"
        "📌 Foydalanish:\n"
        "1️⃣ YouTube video havolasini yuboring\n"
        "2️⃣ Format tanlang (MP4/MP3/WebM)\n"
        "3️⃣ Sifatni tanlang\n"
        "4️⃣ Yuklab oling!\n\n"
        "/help - Yordam\n"
        "/about - Bot haqida"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam buyrug'i"""
    await update.message.reply_text(
        "📖 <b>Yordam</b>\n\n"
        "🔗 YouTube havolasini yuboring va men sizga quyidagi formatlarni taklif qilaman:\n\n"
        "🎥 <b>Video formatlar:</b>\n"
        "  • MP4 - 360p, 480p, 720p, 1080p\n"
        "  • WebM - yuqori sifat\n\n"
        "🎵 <b>Audio formatlar:</b>\n"
        "  • MP3 - 128kbps, 192kbps, 320kbps\n"
        "  • M4A - AAC format\n\n"
        "⚠️ <b>Eslatma:</b> Katta fayllar biroz vaqt olishi mumkin.",
        parse_mode="HTML",
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot haqida"""
    await update.message.reply_text(
        "🤖 <b>YouTube Downloader Bot</b>\n\n"
        "📌 Versiya: 1.0.0\n"
        "🛠 Yaratuvchi: @men_uchun\n"
        "📦 Kutubxona: yt-dlp\n\n"
        "Bu bot YouTube videolarini turli format va sifatlarda yuklab olish imkonini beradi.",
        parse_mode="HTML",
    )


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """YouTube URL qabul qilish"""
    url = update.message.text.strip()

    # URL tekshirish
    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text(
            "❌ Noto'g'ri havola!\n\n"
            "Iltimos, to'g'ri YouTube havolasini yuboring.\n"
            "Masalan: https://youtube.com/watch?v=... yoki https://youtu.be/..."
        )
        return

    msg = await update.message.reply_text("⏳ Video ma'lumotlari yuklanmoqda...")

    try:
        info = get_video_info(url)
        if not info:
            await msg.edit_text("❌ Video topilmadi yoki xususiy video.")
            return

        # Foydalanuvchi ma'lumotlarini saqlash
        user_id = update.effective_user.id
        user_data_store[user_id] = {"url": url, "info": info}

        duration = info.get("duration", 0)
        minutes = duration // 60
        seconds = duration % 60

        # Format tanlash klaviaturasi
        keyboard = [
            [
                InlineKeyboardButton("🎥 MP4 (Video)", callback_data="fmt_mp4"),
                InlineKeyboardButton("🎵 MP3 (Audio)", callback_data="fmt_mp3"),
            ],
            [
                InlineKeyboardButton("📹 WebM (Video)", callback_data="fmt_webm"),
                InlineKeyboardButton("🎶 M4A (Audio)", callback_data="fmt_m4a"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await msg.edit_text(
            f"✅ <b>Video topildi!</b>\n\n"
            f"📌 <b>Sarlavha:</b> {info.get('title', 'Noma\\'lum')[:60]}\n"
            f"👤 <b>Kanal:</b> {info.get('uploader', 'Noma\\'lum')}\n"
            f"⏱ <b>Davomiyligi:</b> {minutes}:{seconds:02d}\n"
            f"👁 <b>Ko'rishlar:</b> {info.get('view_count', 0):,}\n\n"
            f"📂 <b>Format tanlang:</b>",
            reply_markup=reply_markup,
            parse_mode="HTML",
        )

    except Exception as e:
        logger.error(f"URL handle xatosi: {e}")
        await msg.edit_text(
            "❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.\n"
            f"Xato: {str(e)[:100]}"
        )


async def handle_format_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Format tanlash"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    fmt = query.data.replace("fmt_", "")

    if user_id not in user_data_store:
        await query.edit_message_text("❌ Sessiya tugadi. Havolani qayta yuboring.")
        return

    user_data_store[user_id]["format"] = fmt

    # Sifat tanlash
    if fmt in ["mp4", "webm"]:
        keyboard = [
            [
                InlineKeyboardButton("📱 360p", callback_data="qual_360"),
                InlineKeyboardButton("💻 480p", callback_data="qual_480"),
            ],
            [
                InlineKeyboardButton("🖥 720p (HD)", callback_data="qual_720"),
                InlineKeyboardButton("📺 1080p (FHD)", callback_data="qual_1080"),
            ],
            [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_format")],
        ]
        quality_text = "🎥 Video sifatini tanlang:"
    else:
        keyboard = [
            [
                InlineKeyboardButton("🔉 128 kbps", callback_data="qual_128"),
                InlineKeyboardButton("🔊 192 kbps", callback_data="qual_192"),
            ],
            [
                InlineKeyboardButton("🎵 320 kbps", callback_data="qual_320"),
                InlineKeyboardButton("⬅️ Orqaga", callback_data="back_format"),
            ],
        ]
        quality_text = "🎵 Audio sifatini tanlang:"

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"✅ Format: <b>{fmt.upper()}</b> tanlandi\n\n{quality_text}",
        reply_markup=reply_markup,
        parse_mode="HTML",
    )


async def handle_quality_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sifat tanlash va yuklab olish"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    quality = query.data.replace("qual_", "")

    if user_id not in user_data_store:
        await query.edit_message_text("❌ Sessiya tugadi. Havolani qayta yuboring.")
        return

    user_info = user_data_store[user_id]
    url = user_info["url"]
    fmt = user_info["format"]
    info = user_info["info"]

    await query.edit_message_text(
        f"⏬ <b>Yuklab olinmoqda...</b>\n\n"
        f"📌 {info.get('title', '')[:50]}\n"
        f"📂 Format: {fmt.upper()} | Sifat: {quality}\n\n"
        f"⏳ Iltimos kuting...",
        parse_mode="HTML",
    )

    try:
        file_path = None

        if fmt in ["mp4", "webm"]:
            file_path = download_video(url, fmt, quality)
        else:
            file_path = download_audio(url, fmt, quality)

        if not file_path or not os.path.exists(file_path):
            await query.edit_message_text("❌ Yuklab olishda xatolik yuz berdi.")
            return

        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB

        await query.edit_message_text(
            f"📤 Fayl yuborilmoqda... ({file_size:.1f} MB)"
        )

        # Faylni yuborish
        with open(file_path, "rb") as f:
            if fmt in ["mp4", "webm"]:
                await context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=f,
                    caption=f"🎬 {info.get('title', '')[:100]}\n\n📂 {fmt.upper()} | {quality}p\n\n🤖 @YTDownloaderBot",
                    supports_streaming=True,
                )
            else:
                await context.bot.send_audio(
                    chat_id=update.effective_chat.id,
                    audio=f,
                    caption=f"🎵 {info.get('title', '')[:100]}\n\n📂 {fmt.upper()} | {quality}kbps\n\n🤖 @YTDownloaderBot",
                    title=info.get("title", "Audio")[:64],
                    performer=info.get("uploader", "YouTube"),
                )

        await query.edit_message_text("✅ Fayl muvaffaqiyatli yuborildi!")

        # Vaqtinchalik faylni o'chirish
        os.remove(file_path)

        # Foydalanuvchi ma'lumotlarini tozalash
        del user_data_store[user_id]

    except Exception as e:
        logger.error(f"Yuklab olish xatosi: {e}")
        await query.edit_message_text(
            f"❌ Xatolik yuz berdi:\n{str(e)[:200]}\n\n"
            "Qayta urinib ko'ring yoki boshqa sifat tanlang."
        )
        if file_path and os.path.exists(file_path):
            os.remove(file_path)


async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Orqaga qaytish"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    if user_id not in user_data_store:
        await query.edit_message_text("❌ Sessiya tugadi. Havolani qayta yuboring.")
        return

    info = user_data_store[user_id]["info"]
    duration = info.get("duration", 0)
    minutes = duration // 60
    seconds = duration % 60

    keyboard = [
        [
            InlineKeyboardButton("🎥 MP4 (Video)", callback_data="fmt_mp4"),
            InlineKeyboardButton("🎵 MP3 (Audio)", callback_data="fmt_mp3"),
        ],
        [
            InlineKeyboardButton("📹 WebM (Video)", callback_data="fmt_webm"),
            InlineKeyboardButton("🎶 M4A (Audio)", callback_data="fmt_m4a"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"✅ <b>Video topildi!</b>\n\n"
        f"📌 <b>Sarlavha:</b> {info.get('title', 'Noma\\'lum')[:60]}\n"
        f"👤 <b>Kanal:</b> {info.get('uploader', 'Noma\\'lum')}\n"
        f"⏱ <b>Davomiyligi:</b> {minutes}:{seconds:02d}\n"
        f"👁 <b>Ko'rishlar:</b> {info.get('view_count', 0):,}\n\n"
        f"📂 <b>Format tanlang:</b>",
        reply_markup=reply_markup,
        parse_mode="HTML",
    )


def main():
    """Botni ishga tushirish"""
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))

    # URL handler (faqat matn xabarlar)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url)
    )

    # Callback handlerlar
    app.add_handler(CallbackQueryHandler(handle_format_selection, pattern="^fmt_"))
    app.add_handler(CallbackQueryHandler(handle_quality_selection, pattern="^qual_"))
    app.add_handler(CallbackQueryHandler(handle_back, pattern="^back_"))

    logger.info("Bot ishga tushdi! ✅")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
