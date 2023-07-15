# Generated by Django 4.2.3 on 2023-07-15 10:10

from django.conf import settings
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('admin', 'Admin'), ('student', 'Student'), ('staff', 'Staff')], default='admin', max_length=8)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, related_name='users', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='users_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=100)),
                ('regno', models.IntegerField(unique=True)),
                ('course', models.CharField(max_length=100)),
                ('section', models.CharField(max_length=4)),
                ('phone_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Phone number must be a 10-digit number.', regex='^\\d{10}$')])),
                ('groups', models.ManyToManyField(blank=True, related_name='student_users', to='auth.group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='student_users_permissions', to='auth.permission')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staffId', models.IntegerField(unique=True)),
                ('department', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Phone number must be a 10-digit number.', regex='^\\d{10}$')])),
                ('groups', models.ManyToManyField(blank=True, related_name='staff_users', to='auth.group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='staff_users_permissions', to='auth.permission')),
            ],
        ),
    ]
