# Generated by Django 4.2 on 2023-04-29 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0014_alter_userphotos_photo_userfollowers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserFollowers',
            new_name='UserFollowings',
        ),
    ]
