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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import User, Post
from .serializers import *
from django.core import serializers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
# from django.contrib.auth.models import User

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def home(request):
    data = {'count': "data"}
    return HttpResponse("<h1>hello</h1>")

@csrf_exempt
def createAdmin(request):
    email = request.GET.get("email")
    print(email)
    User.objects.create_superuser(
        username="admin",
        last_name="admin",
        first_name="admin",
        email=email,
        password="1234",
        user_type="admin",
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
            else:
                return Response({
                    'error' : 'user type is invalid'
                })
            if serializer.is_valid(raise_exception=ValueError):
                # userSerializer.save()
                print("is valid club user")
                serializer.save()
                print("is valid club user 2 ")
                return Response(
                    userSerializer.data,
                    status=status.HTTP_201_CREATED
                )
                
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
                        "email" : email                     
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

    return Response({"token" : token.key,
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
        data["description"] = request.data.get("description")
        data["postType"] = request.data.get("postType")
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
    allPosts = post.likes.all();
    likes = len(allPosts)
    userLiked = False
    if user in allPosts:
        userLiked = True
    
    # userLiked = post.likes.get(user = user);
    return {
        "id" : post.id,
        "postimg": post.postImage.url,
        "description" : post.description,
        "postType" : post.postType,
        "created" : post.created,
        "likes" : likes,
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
