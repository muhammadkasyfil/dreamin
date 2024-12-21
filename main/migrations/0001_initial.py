# Generated by Django 5.0 on 2024-12-21 02:29

import django.db.models.deletion
import main.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dialogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(blank=True, null=True, upload_to='dialogues')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DreamAnimation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(blank=True, null=True, upload_to='animations', validators=[main.models.validate_file_size, main.models.validate_file_extension])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DreamSound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(blank=True, null=True, upload_to='sounds')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('preview_video', models.FileField(blank=True, null=True, upload_to='dream_previews/')),
                ('dialogues', models.ManyToManyField(blank=True, to='main.dialogue')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dreams', to=settings.AUTH_USER_MODEL)),
                ('animations', models.ManyToManyField(blank=True, to='main.dreamanimation')),
                ('sounds', models.ManyToManyField(blank=True, to='main.dreamsound')),
            ],
        ),
        migrations.CreateModel(
            name='DreamSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('dream', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.dream')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_session_key', models.CharField(blank=True, max_length=40, null=True)),
                ('session_start', models.DateTimeField(blank=True, null=True)),
                ('session_expiry', models.DateTimeField(blank=True, null=True)),
                ('login_count', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reflection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reflections', to='main.dream')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
