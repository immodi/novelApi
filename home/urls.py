from django.urls import path
from home.views import HomeView, DownloadView, FileDataView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('download', DownloadView.as_view(), name="download"),
    path('file-data', FileDataView.as_view(), name="data"),
]

