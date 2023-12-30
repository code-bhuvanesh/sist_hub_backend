from django.urls import path
from .views import *
<<<<<<< HEAD

=======
>>>>>>> ae4c81a8c84902e75efead5aa94c135ac3268030

urlpatterns = [
    # path('', home, name='home'),
    path('createadmin/', createAdmin, name='create admin'),
    path('users/', UserRecordView.as_view(), name='users'),
    path("login/", UserLoginView.as_view(), name="login"),
    path("getuser/", GetUserDetials.as_view(), name="get_user"),
    path("delete_user/", delete_user, name="delete_user"),
    path("addposts/", AddPosts.as_view(), name="add_posts"),
    path("getposts/", GetPosts.as_view(), name="get_posts"),
    path("addcomments/", AddPostComments.as_view(), name="add_comments"),
    path("getcomments/", GetPostComments.as_view(), name="get_comments"),
    path("likeunlikepost/", LikeOrUnlikePost.as_view(), name="get_posts"),
    path("createbus/", CreateBus.as_view(), name="add driver")
    # path("login/", Login.as_view(), name="login")
]

