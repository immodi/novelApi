from home.models import Chunk
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from os import remove, getcwd
from telebot import TeleBot

def handle_uploaded_file(chunk, parent_file, bot, chat_name):
    file_name = chunk.name
    media_dir_path = Path(getcwd(), "novelApi", "media")
    # media_dir_path = Path(getcwd(), "media")
    file_storage = FileSystemStorage(location=media_dir_path)
    file_path = file_storage.save(file_name, chunk)
    full_path = str(Path(media_dir_path, file_path))
    handle_sending_chunk(full_path, chat_name, bot, parent_file)
    remove(full_path)


def handle_sending_chunk(file_path, chat_name, bot: TeleBot, parent_file):
    chat = {
        "novel": -4087357016,
        "drive": -4072410444
    }
    with open(file_path, "rb") as file:
        mes = bot.send_document(chat_id=chat.get(chat_name), document=file, timeout=9999)
        file_id = mes.json.get(list(dict(mes.json).keys())[-1]).get("file_id")
        name = mes.json.get(list(dict(mes.json).keys())[-1]).get("file_name")
        chunck = Chunk(file_id=file_id, main_file=parent_file, name=name)
        chunck.save()
