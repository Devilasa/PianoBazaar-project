# Generated by Django 5.1.4 on 2024-12-10 12:53

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Copy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateField(auto_now_add=True)),
                ('quantity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)])),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sheetmusic.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, default=(4, 99), max_digits=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(300)])),
                ('scoring', models.CharField(choices=[('piano', 'piano solo')], max_length=50)),
                ('type', models.CharField(choices=[('cover', 'Cover'), ('mash-up', 'Mash-up'), ('composition', 'Composition')], max_length=50)),
                ('genre_1', models.CharField(choices=[('classical', 'Classical'), ('jazz', 'Jazz'), ('blues', 'Blues'), ('pop', 'Pop'), ('rock', 'Rock'), ('latin', 'Latin'), ('reggae', 'Reggae'), ('epic', 'Epic'), ('experimental', 'Experimental'), ('videogame', 'Videogame Music'), ('movie/TV', 'Movie/TV'), ('love', 'Love'), ('easy listening', 'Easy Listening'), ('study music', 'Study Music'), ('relax', 'Relax'), ('other', 'Other')], max_length=50)),
                ('genre_2', models.CharField(blank=True, choices=[('classical', 'Classical'), ('jazz', 'Jazz'), ('blues', 'Blues'), ('pop', 'Pop'), ('rock', 'Rock'), ('latin', 'Latin'), ('reggae', 'Reggae'), ('epic', 'Epic'), ('experimental', 'Experimental'), ('videogame', 'Videogame Music'), ('movie/TV', 'Movie/TV'), ('love', 'Love'), ('easy listening', 'Easy Listening'), ('study music', 'Study Music'), ('relax', 'Relax'), ('other', 'Other')], max_length=50)),
                ('published_key', models.CharField(choices=[('C', 'C major'), ('A-', 'A minor'), ('G', 'G major (1 sharp)'), ('E-', 'E minor (1 sharp)'), ('D', 'D major (2 sharps'), ('B-', 'B minor (2 sharps)'), ('A', 'A major (3 sharps)'), ('F#-', 'F# minor (3 sharps)'), ('E', 'E major (4 sharps)'), ('C#-', 'C# minor (4 sharps)'), ('B', 'B major (5 sharps)'), ('G#-', 'G# minor (5 sharps)'), ('F#', 'F# major (6 sharps)'), ('D#-', 'D# minor (6 sharps)'), ('C#', 'C# major (7 sharps)'), ('A#-', 'A# minor (7 sharps)'), ('F', 'F major (1 flat'), ('D-', 'D minor (1 flat)'), ('Bb', 'Bb major (2 flats)'), ('G-', 'G minor (2 flats)'), ('Eb', 'Eb major (3 flats)'), ('C-', 'C minor (3 flats)'), ('Ab', 'Ab major (4 flats)'), ('F-', 'F minor (4 flats)'), ('Db', 'Db major (5 flats)'), ('Bb-', 'Bb minor (5 flats)'), ('Gb', 'Gb major (6 flats)'), ('Eb-', 'Eb minor (6 flats)'), ('Cb', 'Cb major (7 flats)'), ('Ab-', 'Ab minor (7 flats)')], max_length=50)),
                ('youtube_id_video', models.CharField(max_length=50)),
                ('pages_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('file', models.FileField(upload_to='scores/')),
                ('Arranger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sheetmusic.profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='purchased_score',
            field=models.ManyToManyField(through='sheetmusic.Copy', to='sheetmusic.score'),
        ),
        migrations.AddField(
            model_name='copy',
            name='score',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sheetmusic.score'),
        ),
    ]
