from django.contrib import admin
from django.urls import path, include
from novels import urls as novels_urls
from home import urls as home_urls
from webtoon import urls as webtoons_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(novels_urls)),
    path('', include(home_urls)),
    path('', include(webtoons_urls)),
]
