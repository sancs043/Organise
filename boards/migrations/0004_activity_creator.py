# Generated by Django 4.1.6 on 2023-02-13 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_rename_kullanici_user_activity_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='boards.user'),
            preserve_default=False,
        ),
    ]
