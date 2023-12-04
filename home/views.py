from django.shortcuts import render
from django.views.generic import TemplateView
from pathlib import Path
from home.models import File
from django.http import StreamingHttpResponse, HttpResponseNotFound
from wsgiref.util import FileWrapper
from .helpers import *
from .forms import UploadFileForm, DownloadForm
import telebot
import requests
from os import remove, environ, path
from glob import glob
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# BOT_TOKEN = environ.get("BOT_TOKEN")
BOT_TOKEN = "6552202144:AAFVE2A3oVwJqiOouGffrAbRTeCJo8WjsGg"
bot = telebot.TeleBot(BOT_TOKEN)

@method_decorator(csrf_exempt, name='dispatch')
class HomeView(TemplateView):
    def get(self, request):
        # Delete all files in 'tmp' folder
        # files = glob('tmp/*')
        # for f in files:
        #     remove(f)

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


class DownloadView(TemplateView):
    def get(self, request):
            template_name = Path("home", "home.html")
            data = File.objects.all()
            context = {
                "files": data,
            }

            return render(request, template_name, context=context)
            
    def post(self, request):
        form = DownloadForm(request.POST)
        if form.is_valid():
            file_id = form.cleaned_data.get("file_id")
            file = File.objects.get(pk=int(file_id))
            all_chunks = file.chunk_set.all()

            for chunk in all_chunks:
                file_location = Path("tmp", chunk.name)
                r = requests.get(bot.get_file_url(chunk.file_id), allow_redirects=True)

                with open(file_location, 'wb+') as new_file:
                    new_file.write(r.content)
                
            merge_file(file.name)

            file_path = Path("tmp", file.name)
            chunk_size = 1024*1
            response = StreamingHttpResponse(
                FileWrapper(open(file_path, 'rb'), chunk_size),
                content_type=file.mime_type
            )
            response["Content-Disposition"] = f"attachment; filename={file.name}"
            response["Content-Length"] =  path.getsize(file_path)

            return response        
        else:
            form = UploadFileForm()
            template_name = Path("home", "home.html")
            data = File.objects.all()
            context = {
                "files": data,
            }

            return render(request, template_name, context=context)

       
