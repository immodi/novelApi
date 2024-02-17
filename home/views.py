from rest_framework.views import APIView
from rest_framework.response import Response
from pathlib import Path
from home.models import File
import telebot
from django.http import FileResponse
from home.helpers import handle_uploaded_file
import requests
from os import environ, getcwd
from glob import glob
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

token = environ.get("BOT_TOKEN")
bot = telebot.TeleBot(token=token)

@method_decorator(csrf_exempt, name='dispatch')
class HomeView(APIView):
    def get(self, request):
        data = File.objects.all()
                
        context = [{
            "fileId": file.id,
            "fileName" : file.name
        } for file in data]

        return Response(context)

    def post(self, request):
        try:
            file_data = request.data
            chunk = request.FILES.get("file")
            parent_name = file_data.get("parentName", None)
            
            if parent_name is None:
                file_name = file_data.get("fileName")
                mime_type = file_data.get("mimeType")
                size = int(file_data.get("size"))
                
                parent_file = File(mime_type=mime_type, name=file_name, size="{:,.2f}mb".format(size/1024/1024))
                parent_file.save()
            else: parent_file = File.objects.get(name=parent_name)

            handle_uploaded_file(chunk, parent_file, bot, "drive")
            response = dict(list(file_data.items())[:-1])

        except Exception as e:
            response = {"error": str(e)}   
    
        return Response(response)

@method_decorator(csrf_exempt, name='dispatch')
class DownloadView(APIView):
    def get(self, request):
        try:
            tmp_dir = Path(getcwd(), "tmp")
            
            files = glob(str(tmp_dir) + "/*")
            for f in files: remove(f)

            chunk_id = request.GET.get("file_id")
            chunk = Chunk.objects.get(pk=int(chunk_id))
            file_path = Path(tmp_dir, chunk.name)

            r = requests.get(bot.get_file_url(chunk.file_id), allow_redirects=True)

            with open(file_path, 'wb+') as new_file:
                new_file.write(r.content)
                
            return FileResponse(open(file_path, 'rb'), as_attachment=True)
        except Exception as e:
            return Response({"error": str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class FileDataView(APIView):
    def get(self, request):
        try:
            parent_file_name = request.GET.get("parentName", None)

            if parent_file_name is None:
                all_files = File.objects.all()
                return Response([{
                    "fileId": file.id,
                    "fileName": file.name,
                    "chunksIds": [chunk.file_id for chunk in file.chunk_set.all()]
                } for file in all_files])
            else: 
                parent_file = File.objects.filter(name=parent_file_name)                
                if parent_file.exists():
                    parent_file = parent_file.first()
                    return Response({
                        "fileId": parent_file.id,
                        "fileName": parent_file.name,
                        "chunksIds": [chunk.file_id for chunk in parent_file.chunk_set.all()]
                    })
                else:
                    raise Exception("File not found")
        except Exception as e:
            return Response({"error": str(e)})

