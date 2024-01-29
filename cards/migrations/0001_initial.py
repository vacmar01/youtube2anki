# Generated by Django 5.0.1 on 2024-01-28 11:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('channel', models.CharField(max_length=200)),
                ('duration', models.IntegerField()),
                ('transcript', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAnwer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.video')),
            ],
        ),
    ]