import os
import telebot
import yt_dlp

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
  raise RuntimeError("يرجى ضبط متغير البيئة BOT_TOKEN قبل تشغيل البوت.")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "أهلاً بيك! 👋\nابعتلي رابط فيديو من تيك توك وأنا هحاول أنزلهولك.",
  )


@bot.message_handler(func=lambda m: True)
def handle_message(message):
  url = message.text.strip()

  if "tiktok.com" not in url and "vm.tiktok.com" not in url:
    bot.reply_to(message, "من فضلك ابعت رابط فيديو صحيح من تيك توك.")
    return

  status_msg = bot.reply_to(message, "⏳ جاري التحميل، استنى ثواني...")

  file_template = "tiktok_video.%(ext)s"
  ydl_opts = {
      "outtmpl": file_template,
      "format": "mp4/best",
      "quiet": True,
  }

  downloaded_file = None
  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(url, download=True)
      downloaded_file = ydl.prepare_filename(info)

    with open(downloaded_file, "rb") as video:
      bot.send_video(message.chat.id, video)

    bot.delete_message(message.chat.id, status_msg.message_id)

  except Exception as e:
    bot.edit_message_text(
        f"❌ حصلت مشكلة أثناء التحميل:\n{e}",
        message.chat.id,
        status_msg.message_id,
    )
  finally:
    if downloaded_file and os.path.exists(downloaded_file):
      os.remove(downloaded_file)


print("البوت شغال دلوقتي...")
bot.infinity_polling(skip_pending=True)
