from django.urls import path
from novels.views import NovelView

urlpatterns = [
    path(r'novels/', NovelView.as_view(), name="novels"),
]

