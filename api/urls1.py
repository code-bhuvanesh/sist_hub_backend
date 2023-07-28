from django.urls import path
from .views import UserRecordView, login, delete_user, home

urlpatterns = [
    path('', home, name='home'),
]