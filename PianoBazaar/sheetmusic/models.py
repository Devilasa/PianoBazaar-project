from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    purchased_score = models.ManyToManyField('Score', through='Copy')

    def __str__(self):
        return self.user.first_name + self.user.last_name


class Score(models.Model):
    PIECE_TYPE_CHOICES = (
        ('cover', 'Cover'),
        ('mash-up', 'Mash-up'),
        ('composition', 'Composition')
    )

    GENRE_CHOICES = (
        ('classical', 'Classical'),
        ('jazz', 'Jazz'),
        ('blues', 'Blues'),
        ('pop', 'Pop'),
        ('rock', 'Rock'),
        ('latin', 'Latin'),
        ('reggae', 'Reggae'),
        ('epic', 'Epic'),
        ('experimental', 'Experimental'),
        ('videogame', 'Videogame Music'),
        ('movie/TV', 'Movie/TV'),
        ('love', 'Love'),
        ('easy listening', 'Easy Listening'),
        ('study music', 'Study Music'),
        ('relax', 'Relax'),
        ('other', 'Other')
    )

    KEY_CHOICES = (
        ('C', 'C major'),
        ('A-', 'A minor'),

        ('G', 'G major (1 sharp)'),
        ('E-', 'E minor (1 sharp)'),

        ('D', 'D major (2 sharps'),
        ('B-', 'B minor (2 sharps)'),

        ('A', 'A major (3 sharps)'),
        ('F#-', 'F# minor (3 sharps)'),

        ('E', 'E major (4 sharps)'),
        ('C#-', 'C# minor (4 sharps)'),

        ('B', 'B major (5 sharps)'),
        ('G#-', 'G# minor (5 sharps)'),

        ('F#', 'F# major (6 sharps)'),
        ('D#-', 'D# minor (6 sharps)'),

        ('C#', 'C# major (7 sharps)'),
        ('A#-', 'A# minor (7 sharps)'),

        ('F', 'F major (1 flat'),
        ('D-', 'D minor (1 flat)'),

        ('Bb', 'Bb major (2 flats)'),
        ('G-', 'G minor (2 flats)'),

        ('Eb', 'Eb major (3 flats)'),
        ('C-', 'C minor (3 flats)'),

        ('Ab', 'Ab major (4 flats)'),
        ('F-', 'F minor (4 flats)'),

        ('Db', 'Db major (5 flats)'),
        ('Bb-', 'Bb minor (5 flats)'),

        ('Gb', 'Gb major (6 flats)'),
        ('Eb-', 'Eb minor (6 flats)'),

        ('Cb', 'Cb major (7 flats)'),
        ('Ab-', 'Ab minor (7 flats)')
    )

    SCORING_CHOICES = (
        ('piano', 'piano solo'),
    )

    title = models.CharField(max_length=50)
    Arranger = models.ForeignKey(Profile, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(300)], default=(4,99))
    scoring = models.CharField(max_length=50, choices=SCORING_CHOICES)
    type = models.CharField(max_length=50, choices=PIECE_TYPE_CHOICES)
    genre_1 = models.CharField(max_length=50, choices=GENRE_CHOICES)
    genre_2 = models.CharField(max_length=50, choices=GENRE_CHOICES, blank=True)
    published_key = models.CharField(max_length=50, choices=KEY_CHOICES)
    youtube_id_video = models.CharField(max_length=50) #ricordati di fare l'estrazione
    #review
    pages_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    file = models.FileField(upload_to='scores/')

class Copy(models.Model):
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now=False, auto_now_add=True)
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(30)])
