# Generated by Django 5.1.4 on 2024-12-30 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheetmusic', '0019_alter_profile_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='copy',
            name='quantity',
        ),
        migrations.AddField(
            model_name='copy',
            name='license',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
