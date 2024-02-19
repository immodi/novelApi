from rest_framework.views import APIView
from rest_framework.response import Response
from home.models import File
from data.forms import FileForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class FileView(APIView):
    def get(self, request):
        try:
            parent_file_name = request.GET.get("fileName", None)

            if parent_file_name is None:
                # all_files = File.objects.all()
                # return Response([{
                #     "fileId": file.id,
                #     "fileName": file.name,
                #     "chunksIds": [chunk.id for chunk in file.chunk_set.all()]
                # } for file in all_files])
                raise Exception("Please provide 'fileName'")
            else:
                parent_file = File.objects.filter(name=parent_file_name)
                if parent_file.exists():
                    parent_file = parent_file.first()
                    return Response({
                        "fileId": parent_file.id,
                        "fileName": parent_file.name,
                        "chunksIds": [{
                            "chunkId": chunk.id,
                            "chunkName": chunk.name
                        } for chunk in parent_file.chunk_set.all()]
                    })
                else:
                    raise Exception("File not found")
        except Exception as e:
            return Response({"error": str(e)})
    
    def post(self, request):
        try:
            form = FileForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get("name")
                size = form.cleaned_data.get("size")
                mime_type = form.cleaned_data.get("mimeType")
                if File.objects.filter(name=name).exists():
                    raise Exception(f"File with name '{name}' already exists")
                else:
                    file = File.objects.create(name=name, size=size, mime_type=mime_type)
                    file.save()

                    response = {
                        "fileId": file.id,
                        "fileName": file.name,
                        "mimeType": file.mime_type
                    }
            else:
                errors = ""
                for error in form.errors:
                    errors += f"field '{error}' is not valid - " 
                raise Exception(errors[:-3])

        except Exception as e:
            response = {"error": str(e)}

        return Response(response)
