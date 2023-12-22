# Generated by Django 4.2.5 on 2023-12-21 08:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=4000)),
                ('by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channel', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=4000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('Channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video', to='streaming.channel')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=4000)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('on', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='streaming.video')),
            ],
        ),
    ]
