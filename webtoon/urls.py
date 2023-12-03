from django.urls import path
from webtoon.views import WebtoonView

urlpatterns = [
    path(r'webtoons/', WebtoonView.as_view(), name="webtoon"),
]

