from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, PermissionsMixin, BaseUserManager

from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self,
                    username,
                    first_name,
                    last_name,
                    email,
                    password,
                    user_type):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have an email address')
        if not email:
            raise ValueError('Users must have an email address')
       
        user = self.model(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email=self.normalize_email(email),
            user_type = user_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,
                    first_name,
                    last_name,
                    email,
                    password,
                    user_type):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email=self.normalize_email(email),
            user_type = user_type,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('staff', 'Staff'),
    ]
    # is_staff = None
    # is_active = None
    # date_joined = None
    user_type = models.CharField(max_length=8, default='admin', choices=USER_TYPE_CHOICES)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    objects = MyUserManager()
    groups = models.ManyToManyField(
        Group,
        related_name='users',  # Specify a custom related_name
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='users_permissions',  # Specify a custom related_name
        blank=True,
    )

    

class Student(models.Model):
    
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be a 10-digit number."
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=100)
    regno = models.IntegerField(unique=True)
    course = models.CharField(max_length=100)
    section = models.CharField(max_length=4)
    phone_number = models.CharField(validators=[phone_regex], max_length=10)

    groups = models.ManyToManyField(
        Group,
        related_name='student_users',  # Specify a custom related_name
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='student_users_permissions',  # Specify a custom related_name
        blank=True,
    )

    
class Staff(models.Model):
    
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be a 10-digit number."
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staffId = models.IntegerField(unique=True)
    department = models.CharField(max_length=100)
    # course_handling = models.CharField(max_length=100)
    # section = models.CharField(max_length=4)
    phone_number = models.CharField(validators=[phone_regex], max_length=10)

    groups = models.ManyToManyField(
        Group,
        related_name='staff_users',  # Specify a custom related_name
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='staff_users_permissions',  # Specify a custom related_name
        blank=True,
    )

