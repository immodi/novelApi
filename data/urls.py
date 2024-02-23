from django.urls import path
from data.views import FileView, DirectoryView

urlpatterns = [
    path('file', FileView.as_view(), name="file-view"),
    path('directory', DirectoryView.as_view(), name="directory-view"),
]

