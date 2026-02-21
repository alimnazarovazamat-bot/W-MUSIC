import telebot
import os
from yt_dlp import YoutubeDL

TOKEN = "8514778612:AAGRmnDOx47oM6wZ5gCoaO_QhZFaxp7Z8zw"
bot = telebot.TeleBot(TOKEN)

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'noplaylist': True,
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Musiqa nomi yoki link yuboring. 🎵")

@bot.message_handler(func=lambda m: True)
def download_music(message):
    query = message.text
    status = bot.reply_to(message, "Yuklanmoqda... 📥")
    
    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        search = f"ytsearch1:{query}" if not query.startswith("http") else query
        
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(search, download=True)
            if 'entries' in info:
                info = info['entries'][0]
            
            file_path = ydl.prepare_filename(info)
            
            bot.edit_message_text("Yuborilmoqda... 📤", message.chat.id, status.message_id)
            
            with open(file_path, 'rb') as audio:
                # Audio sifatida yuborish, xato bersa hujjat sifatida
                try:
                    bot.send_audio(message.chat.id, audio, caption=f"✅ {info.get('title', 'Musiqa')}")
                except:
                    audio.seek(0)
                    bot.send_document(message.chat.id, audio, caption=f"✅ {info.get('title', 'Musiqa')}")
            
            os.remove(file_path)
            bot.delete_message(message.chat.id, status.message_id)

    except Exception as e:
        print(f"Xato: {e}")
        bot.edit_message_text(f"Xato yuz berdi. Qayta urinib ko'ring.", message.chat.id, status.message_id)

bot.infinity_polling()
