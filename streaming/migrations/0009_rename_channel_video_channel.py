# Generated by Django 4.2.5 on 2023-12-29 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0008_rename_date_video_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='Channel',
            new_name='channel',
        ),
    ]