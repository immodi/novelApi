from django.contrib import admin
from django.urls import path, include
from home import urls as home_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(home_urls)),
]
