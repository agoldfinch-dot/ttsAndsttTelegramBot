import os

from aiogram import Bot, Dispatcher, executor, types
from gtts import gTTS
from translate import Translator
import speech_recognition as sr
from pydub import AudioSegment

API_TOKEN = ""

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(content_types=["voice","video_note"])
async def toText(message: types.Message):
    if message.content_type == "voice":
        await message.voice.download(destination_file="audio.ogg")
    if message.content_type == "video_note":
        await message.video_note.download(destination_file="audio.ogg")
    x = AudioSegment.from_file("audio.ogg")
    x.export("audio.wav", format='wav')   
    r = sr.Recognizer()

    with sr.AudioFile("audio.wav") as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data,language="ru-RU")
        await message.reply(text)
    os.remove("audio.wav")
    os.remove("audio.ogg")
    

@dp.message_handler(commands=['trans','перевод'])
async def translate(message: types.Message):
    lang = message.text.split(' ')[1]
    translator = Translator(from_lang="autodetect", to_lang=lang)
    translation = translator.translate(message.reply_to_message.text)
    tts = gTTS(translation,lang=lang)
    tts.save('voice.ogg')
    await message.reply_voice(open("voice.ogg",'rb'))
    os.remove("voice.ogg")

@dp.message_handler(commands=['озвуч','tts'])
async def TTS(message: types.Message):
    try:
        lang = message.text.split(' ')[1]
        tts = gTTS(message.reply_to_message.text,lang=lang)
        tts.save('voice.ogg')
        await message.reply_voice(open("voice.ogg",'rb'))
        os.remove('voice.ogg')
    except Exception:
        tts = gTTS(message.reply_to_message.text,lang="ru")
        tts.save('voice.ogg')
        await message.reply_voice(open("voice.ogg",'rb'))
        os.remove('voice.ogg')

executor.start_polling(dp, skip_updates=True)