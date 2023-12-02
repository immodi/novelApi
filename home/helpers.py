from filesplit.split import Split
from filesplit.merge import Merge
from home.models import Chunk, File
from pathlib import Path
from os import mkdir, remove
from glob import glob


def handle_uploaded_file(f, bot):
    dir_name = Path("media", str(f).split(".")[0])
    file_path = Path(dir_name, str(f))
    main_file = File(mime_type="none", name=str(f), size="none")
    main_file.save()

    try: mkdir(dir_name)
    except OSError: pass
    
    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    split = Split(file_path, dir_name)
    split.bysize(25*1024*1024)
    remove(file_path)
    
    handle_sending_chunks(bot, dir_name, main_file)
    

def merge_file(f):
    # file_name = str(f).split(".")[0]
    input_dir = "tmp"
    merge = Merge(input_dir, input_dir, str(f))
    merge.merge(True)


def handle_sending_chunks(bot, dir, main_parent, total_size=0, parent_mime_type=""):
    files = glob(f"{dir}/*")

    for file_path in files:
        print(f"Currently processing {file_path}")

        with open(file_path, "rb") as file:
            mes = bot.send_document(chat_id=-4087357016, document=file, timeout=9999)
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