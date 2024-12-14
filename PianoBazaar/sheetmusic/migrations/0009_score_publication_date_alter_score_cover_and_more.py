# Generated by Django 5.1.4 on 2024-12-14 17:18

import django.utils.timezone
import sheetmusic.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheetmusic', '0008_alter_score_cover_alter_score_pages'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='publication_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='score',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to='media/scores/covers'),
        ),
        migrations.AlterField(
            model_name='score',
            name='file',
            field=models.FileField(null=True, upload_to='media/scores/files/', validators=[sheetmusic.models.validate_pdf]),
        ),
        migrations.AlterField(
            model_name='score',
            name='published_key',
            field=models.CharField(choices=[('C', 'C major'), ('A minor', 'A minor'), ('G', 'G major (1 sharp)'), ('E minor', 'E minor (1 sharp)'), ('D', 'D major (2 sharps'), ('B minor', 'B minor (2 sharps)'), ('A', 'A major (3 sharps)'), ('F# minor', 'F# minor (3 sharps)'), ('E', 'E major (4 sharps)'), ('C# minor', 'C# minor (4 sharps)'), ('B', 'B major (5 sharps)'), ('G# minor', 'G# minor (5 sharps)'), ('F#', 'F# major (6 sharps)'), ('D# minor', 'D# minor (6 sharps)'), ('C#', 'C# major (7 sharps)'), ('A# minor', 'A# minor (7 sharps)'), ('F', 'F major (1 flat'), ('D minor', 'D minor (1 flat)'), ('Bb', 'Bb major (2 flats)'), ('G minor', 'G minor (2 flats)'), ('Eb', 'Eb major (3 flats)'), ('C minor', 'C minor (3 flats)'), ('Ab', 'Ab major (4 flats)'), ('F minor', 'F minor (4 flats)'), ('Db', 'Db major (5 flats)'), ('Bb minor', 'Bb minor (5 flats)'), ('Gb', 'Gb major (6 flats)'), ('Ebm minor', 'Eb minor (6 flats)'), ('Cb', 'Cb major (7 flats)'), ('Ab minor', 'Ab minor (7 flats)')], max_length=50),
        ),
        migrations.AlterField(
            model_name='score',
            name='score_type',
            field=models.CharField(choices=[('public domain', 'Public Domain'), ('cover', 'Cover'), ('mash-up', 'Mash-up'), ('composition', 'Original Composition')], max_length=50),
        ),
        migrations.AlterField(
            model_name='score',
            name='scoring',
            field=models.CharField(choices=[('piano', 'Piano solo')], max_length=50),
        ),
    ]
