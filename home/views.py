from rest_framework.views import APIView
from rest_framework.response import Response
from home.models import File, Directory
from home.helpers import handle_uploaded_file
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import telebot
import environ

env = environ.Env()
environ.Env.read_env()

token = env("BOT_TOKEN")
bot = telebot.TeleBot(token=token)

@method_decorator(csrf_exempt, name='dispatch')
class HomeView(APIView):
    def get(self, request):
        dir_id = request.GET.get("dirId", 1)
        current_directory = Directory.objects.filter(pk=dir_id).first() 
        all_dirs = current_directory.directory_set.all()
       
        response = {
            "dirsArray": [{
                "dirId": dir.id,
                "dirPath": dir.path,
            } for dir in all_dirs],

            "filesArray": [{
                "fileId": file.id,
                "fileName": file.name,
                "fileSize": file.size,
            } for file in current_directory.file_set.all()]
        }
        return Response(response)

    def post(self, request):
        try:
            file_data = request.data
            chunk = request.FILES.get("file")
            parent_id = file_data.get("fileId", None)

            if parent_id is None:
                raise Exception("Please provide 'fileId'")
            else:
                parent_id = int(parent_id) 
                parent_file = File.objects.get(pk=parent_id)

            handle_uploaded_file(chunk, parent_file, bot, "drive")
            response = dict(list(file_data.items())[:-1])
        except Exception as e:
            response = {"error": str(e)}

        return Response(response)
