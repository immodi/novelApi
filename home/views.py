from django.shortcuts import render
from django.views.generic import TemplateView
from pathlib import Path
from home.models import File
from django.http import FileResponse, HttpResponseNotFound
from .helpers import *
from .forms import UploadFileForm
import telebot
import requests
from os import remove, environ
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

        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            handle_uploaded_file(request.FILES["file"], bot, "drive")
        else:
            form = UploadFileForm()

        context = {
            "files": data,
        }
        
        return render(request, template_name, context=context)


class DownloadView(TemplateView):
    def get(self, request):
        file = File.objects.get(pk=int(request.GET.get('id', None)))
        all_chunks = file.chunk_set.all()

        for chunk in all_chunks:
            file_location = Path("tmp", chunk.name)
            r = requests.get(bot.get_file_url(chunk.file_id), allow_redirects=True)

            with open(file_location, 'wb+') as new_file:
                new_file.write(r.content)
            
        merge_file(file.name)

        try:    
            response = FileResponse(open(Path("tmp", file.name), 'rb'))
            response.headers['Content-Disposition'] = 'attachment; filename={}'.format(file.name)
            # response.headers['Content-Type'] = file.mime_type
            response.headers['Content-Type'] = "application/octet-stream"
        except IOError:
            response = HttpResponseNotFound('<h1>File not exist</h1>')
        return response
    
