from django.contrib import admin
from django.urls import path, include
from home import urls as home_urls
from data import urls as data_urls
from download import urls as download_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(home_urls)),
    path('', include(data_urls)),
    path('', include(download_urls)),
]
