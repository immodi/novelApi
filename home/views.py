from django.shortcuts import render
from django.views.generic import TemplateView
from pathlib import Path
from home.models import File
from django.http import FileResponse, JsonResponse
from .helpers import *
from .forms import UploadFileForm, DownloadFileForm
import telebot
import requests
from os import remove, environ, path, getcwd
from glob import glob
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

BOT_TOKEN = environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@method_decorator(csrf_exempt, name='dispatch')
class HomeView(TemplateView):
    def get(self, request):
        # Delete all files in 'tmp' folder
        files = glob('tmp/*')
        for f in files:
            remove(f)

        data = File.objects.all()
        template_name = Path("home", "home.html")
        
        context = {
            "files": data
        } 

        return render(request, template_name, context=context)

    def post(self, request):
        template_name = Path("home", "home.html")
        data = File.objects.all()
        context = {
            "files": data,
        }

        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            handle_uploaded_file(request.FILES["file"], bot, "drive")
        else:
            form = UploadFileForm()

        
        return render(request, template_name, context=context)

@method_decorator(csrf_exempt, name='dispatch')
class DownloadView(TemplateView):
    def get(self, request):
        file_id = request.GET.get("file_id")
        file = File.objects.get(pk=int(file_id))
        all_chunks = file.chunk_set.all()

        for chunk in all_chunks:
            file_location = Path("tmp", chunk.name)
            r = requests.get(bot.get_file_url(chunk.file_id), allow_redirects=True)

            with open(file_location, 'wb+') as new_file:
                new_file.write(r.content)
            
        merge_file(file.name)
        file_path = Path(getcwd(), "tmp", file.name)
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        return response
