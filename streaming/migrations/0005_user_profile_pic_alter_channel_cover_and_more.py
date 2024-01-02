# Generated by Django 4.2.5 on 2023-12-25 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0004_channel_cover_video_thumbnail_video_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.FileField(blank=True, default=None, null=True, upload_to='images/pp'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='cover',
            field=models.FileField(blank=True, default=None, null=True, upload_to='images/cover'),
        ),
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.FileField(blank=True, default=None, null=True, upload_to='images/thumbnail'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(blank=True, default=None, null=True, upload_to='videos/'),
        ),
    ]