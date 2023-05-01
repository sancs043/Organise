# Generated by Django 4.1.6 on 2023-04-30 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0013_alter_activity_description_userphotos_userfollowings'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfollowings',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='userfollowings',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='boards.user2'),
        ),
        migrations.AlterField(
            model_name='userfollowings',
            name='following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='boards.user2'),
        ),
        migrations.RemoveField(
            model_name='userfollowings',
            name='created_at',
        ),
    ]
