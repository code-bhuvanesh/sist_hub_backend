import json
from django.http import HttpResponse
from django.shortcuts import render
from api.auth_backend import EmailBackend
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes,renderer_classes
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import User, Post
from .serializers import *
from django.core import serializers
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
# from django.contrib.auth.models import User

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def home(request):
    # User.objects.filter(user_type = "admin").update(is_staff = True, is_superuser = True )
    # User.objects.create_user(
    #     username = "testdriver",
    #     first_name = "test",
    #     last_name = "driver",
    #     email = "testdriver@sist.com",
    #     password ="1234",
    #     user_type = "driver"
    # )
   
    ## delete all bus user
    # for u in User.objects.filter(user_type = "driver"):
    #     print("delted")
    #     u.delete()


    return HttpResponse("<h1>SIST HUB</h1>")

@csrf_exempt
def createAdmin(request):
    email = request.POST.get("email")
    # User.objects.get(username = "admin").delete()
    print(email)
    User.objects.create_superuser(
        username="admin1",
        last_name="admin1",
        first_name="admin1",
        email=email,
        password="1234",
        
    )
    return Response({"email": "user"})

class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users whereas
    a POST request allows to create a new user.
    """
    permission_classes = [AllowAny]
    
    def get(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        # print("users")
        # print(serializer.data)
        return Response(serializer.data)
  
    def post(self, request):
        # User.objects.get(username = "testdriver").delete()
        userSerializer = UserSerializer(data=request.data)
        if userSerializer.is_valid(raise_exception=ValueError):
            user = userSerializer.save()
            
            serializer = None
            serializerData =  dict(request.data)
            serializerData['user'] = user.pk
            if request.data["user_type"] == 'student':
                print("user type student")
                serializer = StudentUserSerializer(data=serializerData)
            elif request.data["user_type"] == 'staff':
                print("user type staff")
                serializer = StaffUserSerializer(data=serializerData)
            elif request.data["user_type"] == 'club':
                print("user type club")
                serializer = ClubUserSerializer(data=serializerData)
            elif request.data["user_type"] == 'driver':
                print("user type bus driver")
                serializer = BusDriverSerializer(data=serializerData)
            else:
                return Response({
                    'error' : 'user type is invalid'
                })
            if serializer.is_valid():
                # userSerializer.save()
                print("is valid club user")
                serializer.save()
                print("is valid club user 2 ")
                return Response(
                    userSerializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                user.delete() 
                serializer.is_valid(raise_exception=ValueError)             
        return Response(
            {
                "error": True,
                "error_msg": userSerializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

#login 
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if email is None or password is None:
            return Response({"error" : "no username or password provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = EmailBackend.authenticate(email=email, password=password)
        if user is None:
            return Response({"error" : "no user found for the given credentials"},
                            status= status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        print(token)

        return Response({"token" : token.key,
                        "email" : email,
                        "id" : user.pk                     
                        },
                        status= status.HTTP_200_OK)

    
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if email is None or password is None:
        return Response({"error" : "no username or password provided"},
                        status=status.HTTP_400_BAD_REQUEST)

    user = EmailBackend.authenticate(email=email, password=password)
    if user is None:
        return Response({"error" : "no user found for the given credentials"},
                        status= status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    print(token)

    return Response(
        {
        "id" : user.pk,
        "token" : token.key,
        "email" : email                     
        },
        status= status.HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def delete_user(request):
    try:
        u = User.objects.get(username = request.data.get("username"))
        u.delete()

    except User.DoesNotExist:
        
        return Response({"error":"does not exist"})

    except Exception as e: 
        return Response({"error":"error"})

    return Response({"error":"deleted"}) 


class AddPosts(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        userId = Token.objects.get(key=request.auth.key).user_id
        data = {}
        data["postContent"] = request.data.get("postContent")
        data["postType"] = request.data.get("postType")
        if request.data.get('postImage') == "":
            data["postImage"] = None
        else:
            data["postImage"] = request.data.get("postImage")

        data["user"] = userId
        # print(request.data)
        postSerializer = PostSerializer(data=data)
        print("post started")
        if postSerializer.is_valid(raise_exception=ValueError):
            post = postSerializer.save()
            
            return Response(
                data={"postid" : post.id},
                status=status.HTTP_200_OK
                )
        return Response(
                data={"postid" : post.id},
                status=status.HTTP_400_BAD_REQUEST
                )

        

class GetPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # print(request.user)
        posts_data = Post.objects.order_by("-created")[:10]
        
        data = []
        # data = json.loads(serializers.serialize("json" , posts_data))
        for post in posts_data:
            post_details = getPostDetails(post, request.user)
            
            data.append(post_details)
        return Response(
            data
        )

def getPostDetails(post, user):
    allPostsLikes = post.likes.all();
    allPostsComments = PostComments.objects.filter(post=post.id)
    likes = len(allPostsLikes)
    comments = len(allPostsComments)
    userLiked = False
    if user in allPostsLikes:
        userLiked = True
    postUrl = ""
    if post.postImage:
        postUrl = post.postImage.url
    # userLiked = post.likes.get(user = user);
    return {
        "id" : post.id,
        "postimg": postUrl,
        "description" : post.postContent,
        "postType" : post.postType,
        "created" : post.created,
        "likes" : likes,
        "comments" : comments,
        "userLiked": userLiked,
        "userId" : post.user.id,
        "username" : post.user.username,
        "userProfileUrl" : None
        }

class LikeOrUnlikePost(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        post_id = request.data.get("postid")
        post = Post.objects.get(id=post_id)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        
        post = Post.objects.get(id=post_id)

        post_details = getPostDetails(post, request.user)
        # data = serializers.serialize("json", post, )
        return Response(data=post_details, status=status.HTTP_200_OK)



def userDetails(user:User, isOwner:bool = False):
    if(isOwner):
        token, _ = Token.objects.get_or_create(user=user)
        return {
            "id" : user.id,
            "username" : user.username,
            "token" : str(token),
            "email" : user.email,
            "usertype" : user.user_type
        }
    else:
        return {
            "id" : user.id,
            "username" : user.username,
            "email" : user.email,
            "usertype" : user.user_type
        }

class GetUserDetials(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        userID = int(request.data.get("userid"))
        user = User.objects.get(id=userID)
        print(user.id)
        isOwner = (request.user.id == userID) 
        print("isOwner : " + str(isOwner))
        if user is None:
            return Response("user not found", status=status.HTTP_404_NOT_FOUND)
        elif isOwner:
            return Response(userDetails(user, True), status=status.HTTP_200_OK)
        else:
            return Response(userDetails(user), status=status.HTTP_200_OK)
    
    

class AddPostComments(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print(type(request.data))
        comment_data = request.data.dict()
        comment_data["user"] = request.user.id
        print(comment_data)
        postCommentSerializer = PostCommentsSerializer(data=comment_data)
        if postCommentSerializer.is_valid(raise_exception=ValueError):
            post = Post.objects.get(id=comment_data["post"])
            post.comments.add(request.user)
            postCommentSerializer.save()
            # comment = PostComments.objects.get(postCommentSerializer.data["id"])
            
            return Response(postCommentSerializer.data, status=status.HTTP_200_OK)
        return Response("cannot add the comment", status=status.HTTP_400_BAD_REQUEST)

class GetPostComments(APIView):
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        postID = request.data.get("postid")
        print(postID)
        comments = PostCommentsSerializer(PostComments.objects.filter(post=postID).order_by("-created"), many=True).data
        print(comments)
        return Response(comments, status=status.HTTP_200_OK)
    

#databse view for Bus

class CreateBus(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        busData = dict(request.data)
        busData["user"] = request.user
        busSerializer = BusSerializer(data=busData)
        if busSerializer.is_valid(raise_exception=ValueError):
            return Response({"status" : "bus created"}, status=status.HTTP_201_CREATED)
        return Response({"status" : "error creating new driver"}, status=status.HTTP_400_BAD_REQUEST)
