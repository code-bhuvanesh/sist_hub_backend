from api.auth_backend import EmailBackend
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
# from django.contrib.auth.models import User


def createAdmin(request):
    email = request.GET.get("email")
    User.objects.create_superuser(
        username="admin",
        last_name="admin",
        first_name="admin",
        email=email,
        password="1234",
        user_type="ADMIN",
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
        print("users")
        print(serializer.data)
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
            else:
                return Response({
                    'error' : 'user type can be only student or staff'
                })
            if serializer.is_valid(raise_exception=ValueError):
                # userSerializer.save()
                serializer.save()
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
class Login(APIView):
    # @csrf_exempt
    # @api_view(["POST"])
    # @permission_classes((AllowAny,))
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if username is None or password is None:
            return Response({"error" : "no username or password provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({"error" : "no user found for the given credentials"},
                            status= status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        print(token)
   
        return Response({"token" : token.key},
                        status= status.HTTP_200_OK)
    
# @csrf_exempt
# @api_view(["POST"])
# @permission_classes((AllowAny,))
# def login(request):
#     email = request.data.get("email")
#     password = request.data.get("password")

#     if email is None or password is None:
#         return Response({"error" : "no username or password provided"},
#                         status=status.HTTP_400_BAD_REQUEST)

#     user = authenticate(email=email, password=password)
#     if user is None:
#         return Response({"error" : "no user found for the given credentials"},
#                         status= status.HTTP_404_NOT_FOUND)
#     token, _ = Token.objects.get_or_create(user=user)
#     print(token)

#     return Response({"token" : token.key},
#                     status= status.HTTP_200_OK)

    
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
