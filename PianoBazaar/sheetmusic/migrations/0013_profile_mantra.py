# Generated by Django 5.1.4 on 2024-12-14 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheetmusic', '0012_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mantra',
            field=models.TextField(blank=True, max_length=100),
        ),
    ]
