# Generated by Django 4.2.6 on 2023-12-19 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_location_location_name_alter_post_postimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='description',
            new_name='postContent',
        ),
    ]
