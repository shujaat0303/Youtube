# Generated by Django 4.2.5 on 2023-12-29 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0007_comment_num_comments_video_num_views_watchhistory_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='date',
            new_name='time',
        ),
    ]
