# Generated by Django 4.2 on 2023-04-29 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0015_rename_userfollowers_userfollowings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]