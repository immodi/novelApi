from rest_framework.views import APIView
from rest_framework.response import Response
from home.models import File, Directory
from data.forms import FileForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class FileView(APIView):
    def get(self, request):
        try:
            file_path = request.GET.get("filePath", None)
            file_id = request.GET.get("fileId", None)
            if file_path is None and file_id is None:
                raise Exception("Please provide 'filePath' or a 'fileId'")
            elif file_id and not file_path:
                parent_file = File.objects.filter(pk=file_id)
                if parent_file.exists():
                    parent_file = parent_file.first()
                    parent_file_dir = parent_file.parent_dir.path
                    return Response({
                        "fileId": parent_file.id,
                        "fileName": parent_file.name,
                        "fileFullPath": parent_file_dir + "/" + parent_file.name,
                        "fileMimeType": parent_file.mime_type,
                        "chunksIds": [{
                            "chunkId": chunk.id,
                            "chunkName": chunk.name
                        } for chunk in parent_file.chunk_set.all()]
                    })
                else:
                    raise Exception(f"File with id {file_id} not found")
            else:
                file_name = file_path.split("/")[-1]
                parent_directory_path = "/".join(file_path.split("/")[:-1])

                parent_directory_filter = Directory.objects.filter(path=parent_directory_path)
                parent_files = File.objects.filter(name=file_name)
                if parent_files.exists() and parent_directory_filter.exists():
                    parent_directory = parent_directory_filter.first()
                    parent_file = parent_files.filter(parent_dir=parent_directory).first()
                    return Response({
                        "fileId": parent_file.id,
                        "fileName": parent_file.name,
                        "fileFullPath": file_path,
                        "fileMimeType": parent_file.mime_type,
                        "chunksIds": [{
                            "chunkId": chunk.id,
                            "chunkName": chunk.name
                        } for chunk in parent_file.chunk_set.all()]
                    })
                else:
                    raise Exception(f"File with path {file_path} not found")
        except Exception as e:
            return Response({"error": str(e)})
    
    def post(self, request):
        try:
            form = FileForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get("name")
                size = form.cleaned_data.get("size")
                mime_type = form.cleaned_data.get("mimeType")
                path = form.cleaned_data.get("path")
                
                dir = Directory.objects.filter(path=path).first()
                if dir is None: raise Exception(f"Directory with name '{path}' does not exist")
                
                if File.objects.filter(name=name, parent_dir=dir).exists():
                    raise Exception(f"File with path '{path}/{name}' already exists")
                else:
                    file = File.objects.create(name=name, size=size, mime_type=mime_type, parent_dir=dir)
                    file.save()

                    response = {
                        "fileId": file.id,
                        "fileName": file.name,
                        "filePath": dir.path + "/" + file.name,
                        "mimeType": file.mime_type,
                    }
            else:
                errors = ""
                for error in form.errors:
                    errors += f"field '{error}' is not valid - " 
                raise Exception(errors[:-3])

        except Exception as e:
            response = {"error": str(e)}

        return Response(response)
    
@method_decorator(csrf_exempt, name='dispatch')
class DirectoryView(APIView):
    def get(self, request):
        dir_path = request.GET.get("dirPath", None)
        if dir_path is not None: 
            dir = Directory.objects.filter(path=dir_path).first()
            if dir is None: return Response({"error": "Directory not found"})
            else:
                return Response({
                    "dirId": dir.id,
                    "dirPath": dir.path
                })
            
        return Response([{
            "dirId": dir.id,
            "dirPath": dir.path
        } for dir in Directory.objects.all()])
        
    def post(self, request):
        dir_path: str = request.GET.get("dirPath", None)
        if dir_path is None: return Response({"error": "Invalid Directory Path 'dirPath'"})

        if Directory.objects.filter(path=dir_path).exists(): 
            return Response({"error": "Directory Exists!"})
        
        parent_dir_path = "/".join(dir_path.split("/")[:-1])
        parent_dir = Directory.objects.filter(path=parent_dir_path).first()
        if parent_dir is None: return Response({"error": "Invalid Parent Directory"})
        
        dir, saved = Directory.objects.get_or_create(path=dir_path, parent_dir=parent_dir)
        if not saved: return Response({"error": "Error saving Directory"})
        else:
            dir.save()
            return Response({
                "dirId": dir.id,
                "dirPath": dir.path
            })
        