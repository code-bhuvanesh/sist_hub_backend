from django.urls import path
from .views import UserRecordView, UserLoginView, AddPosts, GetPosts,login, delete_user, createAdmin
from .views import UserRecordView, Login, login, delete_user, home

urlpatterns = [
    path('', home, name='home'),
    path('users/', UserRecordView.as_view(), name='users'),
    path("login/", UserLoginView.as_view(), name="login"),
    path("delete_user/", delete_user, name="delete_user"),
    path("addposts/", AddPosts.as_view(), name="add_posts"),
    path("getposts/", GetPosts.as_view(), name="get_posts")
    # path("login/", Login.as_view(), name="login")
]