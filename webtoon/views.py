from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.generic import TemplateView
from pathlib import Path
from .forms import WebtoonsForm
from filesplit.split import Split
from .app.main import WebtoonScrapper 
from home.models import File
from home.helpers import *
import telebot
from os import remove, environ, mkdir
from shutil import rmtree
from glob import glob
from re import sub

BOT_TOKEN = environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


@method_decorator(csrf_exempt, name='dispatch')
class WebtoonView(TemplateView):
    def get(self, request):
        template_name = Path("webtoon", "webtoon.html")
        return render(request, template_name)

    def post(self, request):
        data = File.objects.all()
        template_name = Path("home", "home.html")
        context = {
            "files": data
        } 

        form = WebtoonsForm(request.POST)
        sources = {
            "Hiperdex": "hiperdex",
            "Manga18fx": "manga18fx",
            "Toonily.net": "toonily",
        } 

        if form.is_valid():
            webtoon_name = sub(r'\W+', '', form.cleaned_data.get("webtoon_name"))
            webtoon_url = form.cleaned_data.get("webtoon_url")
            start_num = int(form.cleaned_data.get("starting_chapter"))
            total_chapters = int(form.cleaned_data.get("total_chapters"))
            source = sources.get(form.cleaned_data.get("webtoon_source"))
            webtoon = WebtoonScrapper(webtoon_name, webtoon_url, start_num, total_chapters, source)
            webtoon.execute()
            webtoon.clean_up()

            dir_name = split_file(webtoon_name, "zip", Path("webtoon", "app"))

            main_file = File(mime_type="none", name=f"{webtoon_name}.zip", size="none")
            main_file.save()

            handle_sending_chunks("novel", bot, dir_name, main_file)
            rmtree(dir_name)        


        return render(request, template_name, context)

