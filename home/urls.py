from django.urls import path
from home.views import HomeView, DownloadView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path(r'download/<str:file_id>', DownloadView.as_view(), name="download"),
]

