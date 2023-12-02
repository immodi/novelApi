import pathlib as path
from django.shortcuts import render
from django.views.generic import TemplateView
from .app.novel_to_book import NovelChaptersLoader
from .forms import NovelsForm
import telebot
# from home.models import File
from filesplit.split import Split
from os import remove
from os import environ
from django.shortcuts import redirect
from pathlib import Path
from shutil import rmtree
from home.helpers import *


BOT_TOKEN = environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


class NovelView(TemplateView):
    def get(self, request):
        template_name = Path("novels", "novels.html")
        return render(request, template_name)
    
    def post(self, request):
        template_name = Path("novels", "novels.html")
        sources = {
            "Bednovel" : 0,
            "All Novel Updates" : 1,
            "Bakapervert" : 2
        }

        form = NovelsForm(request.POST)
        # for field in form:
            # print("Field Error:", field.name,  field.errors)

        if form.is_valid():
            novel_name = form.cleaned_data.get("novel_name")
            novel_url = form.cleaned_data.get("novel_url")
            start_num = int(form.cleaned_data.get("starting_chapter"))
            source = sources.get(form.cleaned_data.get("novel_source"))
            novel = NovelChaptersLoader(novel_name, novel_url, start_num, source)
            novel.execute()
            
            dir_name = path.Path("novels", "app", novel_name)
            file_path = path.Path("novels", "app", f"{novel_name}.pdf")

            try: mkdir(dir_name)
            except OSError: pass 
             
            split = Split(file_path, dir_name)
            split.bysize(25*1024*1024)
            remove(file_path)
            
            main_file = File(mime_type="none", name=f"{novel_name}.pdf", size="none")
            main_file.save()

            handle_sending_chunks("drive", bot, dir_name, main_file)
            rmtree(dir_name)        
                

        return redirect("/")
                    
    
# def send_file(file):
#     mes = bot.send_document(chat_id=-4087357016, document=file)
#     # file_id = mes.json.get("document").get("file_id")
#     name = mes.json.get("document").get("file_name")
#     mime_type = mes.json.get("document").get("mime_type")
#     size = "{:,.2f}mb".format(float(mes.json.get("document").get("file_size"))/1024/1024)
#     # file = File(file_id=file_id, name=name, mime_type=mime_type, size=size)
#     # file.save()
