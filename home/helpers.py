from filesplit.split import Split
from filesplit.merge import Merge
from home.models import Chunk, File
from pathlib import Path
from os import mkdir, remove
from glob import glob
from re import sub

def handle_uploaded_file(f, bot, chat_name):
    file_name = sub(r'\W+', ' ', str(f))
    dir_name = Path("media", file_name.split(".")[0])
    file_path = Path(dir_name, file_name)
    main_file = File(mime_type="none", name=file_name, size="none")
    main_file.save()

    try: mkdir(dir_name)
    except OSError: pass
    
    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    split = Split(file_path, dir_name)
    split.bysize(20*1024*1024)
    remove(file_path)
    
    handle_sending_chunks(chat_name, bot, dir_name, main_file)
    

def split_file(file_name, file_extention, dir_path):
    dir_name = Path(dir_path, f"{file_name}_chunks")
    file_path = Path(dir_path, f"{file_name}.{file_extention}")

    try: mkdir(dir_name)
    except OSError: pass 
        
    split = Split(file_path, dir_name)
    split.bysize(20*1024*1024)
    remove(file_path)
    return dir_name

def merge_file(f):
    # file_name = str(f).split(".")[0]
    input_dir = "tmp"
    merge = Merge(input_dir, input_dir, str(f))
    merge.merge(True)


def handle_sending_chunks(chat_name, bot, dir, main_parent, total_size=0, parent_mime_type=""):
    chat = {
        "novel": -4087357016,
        "drive": -4072410444
    }

    files = glob(f"{dir}/*")

    for file_path in files:
        print(f"Currently processing {file_path}")

        with open(file_path, "rb") as file:
            mes = bot.send_document(chat_id=chat.get(chat_name), document=file, timeout=9999)
            if mes.json.get("document").get("mime_type"): 
                mime_type = mes.json.get("document").get("mime_type")
                parent_mime_type = mime_type
            else: mime_type = ""
            file_id = mes.json.get("document").get("file_id")
            name = mes.json.get("document").get("file_name")
            total_size += float(mes.json.get("document").get("file_size"))
            chunck = Chunk(file_id=file_id, name=name, mime_type=mime_type, main_file=main_parent)
            chunck.save()
            
    main_parent.mime_type = parent_mime_type
    main_parent.size = "{:,.2f}mb".format(total_size/1024/1024)
    main_parent.save()