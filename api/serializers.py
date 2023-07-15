# from .models import User
# from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'user_type'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
    
    def create(self, validated_data):
        username = validated_data.get("username")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        email = validated_data.get("email")
        password = validated_data.get("password")
        user_type = validated_data.get("user_type")

        user = User.objects.create_superuser(username, first_name, last_name, email, password, user_type)
        return user

class StudentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = (
            'user',
            'regno',
            'phone_number',
            'branch',
            'course',
            'section',        
        )

        validators = [
            UniqueTogetherValidator(
                queryset=Student.objects.all(),
                fields=[ 'regno', 'user']
            )
        ]

class StaffUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = (
            'user',
            'staffId',
            'phone_number',
        )

        validators = [
            UniqueTogetherValidator(
                queryset=Staff.objects.all(),
                fields=['staffId', 'user']
            )
        ]

