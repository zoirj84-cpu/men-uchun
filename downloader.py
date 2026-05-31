import yt_dlp
import os
import tempfile
import logging

logger = logging.getLogger(__name__)

# Vaqtinchalik fayl saqlash papkasi
DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), "yt_bot_downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def get_video_info(url: str) -> dict | None:
    """YouTube video ma'lumotlarini olish"""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", "Noma'lum"),
                "uploader": info.get("uploader", "Noma'lum"),
                "duration": info.get("duration", 0),
                "view_count": info.get("view_count", 0),
                "thumbnail": info.get("thumbnail", ""),
                "description": info.get("description", "")[:200],
            }
    except Exception as e:
        logger.error(f"Video ma'lumot olishda xato: {e}")
        return None


def download_video(url: str, fmt: str = "mp4", quality: str = "720") -> str | None:
    """Video yuklab olish"""
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    # Sifat sozlamalari
    quality_map = {
        "360": "bestvideo[height<=360]+bestaudio/best[height<=360]",
        "480": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        "720": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "1080": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    }

    format_str = quality_map.get(quality, quality_map["720"])

    ydl_opts = {
        "format": format_str,
        "outtmpl": output_path,
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": fmt,
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": fmt,
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "video")

            # Fayl nomini topish
            for file in os.listdir(DOWNLOAD_DIR):
                if file.endswith(f".{fmt}"):
                    file_path = os.path.join(DOWNLOAD_DIR, file)
                    if os.path.getsize(file_path) > 0:
                        return file_path

            # Agar to'g'ri topilmasa, barcha fayllarni tekshirish
            for file in os.listdir(DOWNLOAD_DIR):
                file_path = os.path.join(DOWNLOAD_DIR, file)
                if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
                    return file_path

    except Exception as e:
        logger.error(f"Video yuklab olishda xato: {e}")
        return None

    return None


def download_audio(url: str, fmt: str = "mp3", quality: str = "192") -> str | None:
    """Audio yuklab olish"""
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    # Audio sifat
    audio_quality_map = {
        "128": "128",
        "192": "192",
        "320": "320",
    }

    audio_quality = audio_quality_map.get(quality, "192")

    # Format sozlamalari
    if fmt == "mp3":
        postprocessors = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": audio_quality,
            }
        ]
    elif fmt == "m4a":
        postprocessors = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
                "preferredquality": audio_quality,
            }
        ]
    else:
        postprocessors = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": fmt,
                "preferredquality": audio_quality,
            }
        ]

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": postprocessors,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            # Fayl nomini topish
            for file in os.listdir(DOWNLOAD_DIR):
                if file.endswith(f".{fmt}"):
                    file_path = os.path.join(DOWNLOAD_DIR, file)
                    if os.path.getsize(file_path) > 0:
                        return file_path

            # Agar topilmasa
            for file in os.listdir(DOWNLOAD_DIR):
                file_path = os.path.join(DOWNLOAD_DIR, file)
                if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
                    return file_path

    except Exception as e:
        logger.error(f"Audio yuklab olishda xato: {e}")
        return None

    return None


def clean_downloads():
    """Eski fayllarni tozalash"""
    try:
        for file in os.listdir(DOWNLOAD_DIR):
            file_path = os.path.join(DOWNLOAD_DIR, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        logger.info("Yuklamalar papkasi tozalandi")
    except Exception as e:
        logger.error(f"Tozalashda xato: {e}")
