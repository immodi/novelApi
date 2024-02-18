from rest_framework.views import APIView
from rest_framework.response import Response
from home.models import File
import telebot
from home.helpers import handle_uploaded_file
from os import environ
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
