from django.urls import path
from .views import UserRecordView, Login, login, delete_user, home

urlpatterns = [
    path('', home, name='home'),
    path('users/', UserRecordView.as_view(), name='users'),
    path("login/", login, name="login"),
    path("delete_user/", delete_user, name="delete_user")
    # path("login/", Login.as_view(), name="login")
]