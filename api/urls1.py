from django.urls import path
from .views import UserRecordView, Login, login, delete_user, home

urlpatterns = [
    path('', home, name='home'),
]