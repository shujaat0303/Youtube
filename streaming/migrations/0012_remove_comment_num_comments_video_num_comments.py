# Generated by Django 4.2.5 on 2024-01-08 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0011_alter_video_thumbnail_alter_video_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='num_comments',
        ),
        migrations.AddField(
            model_name='video',
            name='num_comments',
            field=models.IntegerField(default=0),
        ),
    ]
