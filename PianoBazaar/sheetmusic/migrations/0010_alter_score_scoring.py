# Generated by Django 5.1.4 on 2024-12-14 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheetmusic', '0009_score_publication_date_alter_score_cover_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='scoring',
            field=models.CharField(choices=[('piano solo', 'Piano solo')], max_length=50),
        ),
    ]
