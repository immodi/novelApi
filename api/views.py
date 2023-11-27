from rest_framework.views import APIView
from django.http import FileResponse
from rest_framework.response import Response
# from rest_framework import status
import pathlib as path
# from os import remove
from .app.novel_to_book import NovelChaptersLoader
import telebot


BOT_TOKEN = ""
bot = telebot.TeleBot(BOT_TOKEN)


class ApiView(APIView):
    def get(self, request):
        novel_name = request.query_params.get('name', None)
        url = request.query_params.get('url', None)
        start_num = int(request.query_params.get('start', 1))
        source = int(request.query_params.get('source', 1))

        if novel_name is None or url is None or start_num is None:
            result = {
                    'params': ("name", "url", "start", "source [default=AllnovelUpdates]"),
                    'error': 'all params are required'
                }
            return Response(result)
        
        novel = NovelChaptersLoader(novel_name, url, start_num, source)
        novel.execute()

        with open(path.Path("api", "app", f"{novel_name}.pdf"), "rb") as file:  send_file(file)
        # remove(path.Path("api", "app", f"{novel_name}.pdf"))

        return Response({"send": True})
        # return FileResponse(file, as_attachment=True, filename=f"{novel_name}.pdf")
    
def send_file(file):
    bot.send_document(chat_id=-4087357016, document=file)
