from django.urls import path
<<<<<<< HEAD
from .views import UserRecordView, UserLoginView, AddPosts, GetPosts,login, delete_user, createAdmin
=======
from .views import UserRecordView, Login, login, delete_user, home
>>>>>>> 615efd02ca02759cd85e3890132a58b44c38c36f

urlpatterns = [
    path('', home, name='home'),
    path('users/', UserRecordView.as_view(), name='users'),
    path("login/", UserLoginView.as_view(), name="login"),
    path("delete_user/", delete_user, name="delete_user"),
    path("addposts/", AddPosts.as_view(), name="add_posts"),
    path("getposts/", GetPosts.as_view(), name="get_posts")
    # path("login/", Login.as_view(), name="login")
]