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
from re import sub
from django.shortcuts import redirect
from pathlib import Path
from shutil import rmtree
from home.helpers import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


BOT_TOKEN = environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


@method_decorator(csrf_exempt, name='dispatch')
class NovelView(TemplateView):
    sources = {
        "Novelhulk" : 0,
    }
    def get(self, request):
        template_name = Path("novels", "novels.html")
        return render(request, template_name, {"sources": self.sources.keys()})
    
    def post(self, request):
        data = File.objects.all()
        template_name = Path("home", "home.html")
        
        context = {
            "files": data
        } 

        form = NovelsForm(request.POST)
        # for field in form:
        #     print("Field Error:", field.name,  field.errors)

        if form.is_valid():
            novel_name = sub(r'\W+', ' ', form.cleaned_data.get("novel_name"))
            novel_url = form.cleaned_data.get("novel_url")
            start_num = int(form.cleaned_data.get("starting_chapter"))
            source = self.sources.get(form.cleaned_data.get("novel_source"))
            novel = NovelChaptersLoader(novel_name, novel_url, start_num, source)
            novel.execute()
            
            dir_name = split_file(novel_name, "pdf", Path("novels", "app"))
            main_file = File(mime_type="none", name=f"{novel_name}.pdf", size="none")
            main_file.save()

            handle_sending_chunks("novel", bot, dir_name, main_file)
            rmtree(dir_name)        
                

        return render(request, template_name, context)
                    
