from django.urls import path
from data.views import FileView

urlpatterns = [
    path('file', FileView.as_view(), name="data"),
]

