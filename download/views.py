from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from pathlib import Path
from home.models import Chunk
from home.views import bot
import requests
from os import getcwd, remove
from glob import glob
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class DownloadView(APIView):
    def get(self, request):
        try:
            # tmp_dir = Path(getcwd(), "tmp")
            tmp_dir = Path(getcwd(), "novelApi", "tmp")

            # remove all files in 'tmp' directory
            files = glob(str(tmp_dir) + "/*")
            for f in files: remove(f)

            chunk_id = request.GET.get("chunkId", None)
            chunk = Chunk.objects.get(pk=int(chunk_id))
            file_path = Path(tmp_dir, chunk.name)

            r = requests.get(bot.get_file_url(chunk.file_id), allow_redirects=True)

            with open(file_path, 'wb+') as new_file:
                new_file.write(r.content)

            return FileResponse(open(file_path, 'rb'), as_attachment=True)
        except Exception as e:
            return Response({"error": str(e)})