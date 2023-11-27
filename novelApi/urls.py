from django.contrib import admin
from django.urls import path, include
import api.urls as api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(api_urls)),
]
