from django.urls import path
from api.views import ApiView

urlpatterns = [
    path('', ApiView.as_view(), name="api"),
]

