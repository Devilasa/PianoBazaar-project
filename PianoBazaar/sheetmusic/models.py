import os.path
import PyPDF2
import fitz

from PyPDF2 import PdfReader
from urllib.parse import urlparse, parse_qs
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from PianoBazaar.settings import BASE_DIR


def validate_pdf(file):
    try:
        PdfReader(file)
    except Exception:
        # File must be in PDF format.
        raise ValidationError('Oops! It seems the uploaded file is not a valid PDF. Make sure to upload a proper PDF file and try again.')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=400, blank=True)
    mantra = models.TextField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.FileField(upload_to='media/profiles/profile_imgs', blank=True, null=True)
    youtube_account_id = models.CharField(max_length=30, blank=True, null=True)
    instagram_account_id = models.CharField(max_length=30, blank=True, null=True)
    x_account_id = models.CharField(max_length=30, blank=True, null=True)
    purchased_scores = models.ManyToManyField('Score', through='Copy', blank=True, related_name='purchased_scores')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Score(models.Model):
    PIECE_TYPE_CHOICES = (
        ('public domain', 'Public Domain'),
        ('cover', 'Cover'),
        ('mash-up', 'Mash-up'),
        ('composition', 'Original Composition')
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
        ('A minor', 'A minor'),

        ('G', 'G major (1 sharp)'),
        ('E minor', 'E minor (1 sharp)'),

        ('D', 'D major (2 sharps'),
        ('B minor', 'B minor (2 sharps)'),

        ('A', 'A major (3 sharps)'),
        ('F# minor', 'F# minor (3 sharps)'),

        ('E', 'E major (4 sharps)'),
        ('C# minor', 'C# minor (4 sharps)'),

        ('B', 'B major (5 sharps)'),
        ('G# minor', 'G# minor (5 sharps)'),

        ('F#', 'F# major (6 sharps)'),
        ('D# minor', 'D# minor (6 sharps)'),

        ('C#', 'C# major (7 sharps)'),
        ('A# minor', 'A# minor (7 sharps)'),

        ('F', 'F major (1 flat'),
        ('D minor', 'D minor (1 flat)'),

        ('Bb', 'Bb major (2 flats)'),
        ('G minor', 'G minor (2 flats)'),

        ('Eb', 'Eb major (3 flats)'),
        ('C minor', 'C minor (3 flats)'),

        ('Ab', 'Ab major (4 flats)'),
        ('F minor', 'F minor (4 flats)'),

        ('Db', 'Db major (5 flats)'),
        ('Bb minor', 'Bb minor (5 flats)'),

        ('Gb', 'Gb major (6 flats)'),
        ('Ebm minor', 'Eb minor (6 flats)'),

        ('Cb', 'Cb major (7 flats)'),
        ('Ab minor', 'Ab minor (7 flats)')
    )

    SCORING_CHOICES = (
        ('piano solo', 'Piano solo'),
    )

    title = models.CharField(max_length=50)
    arranger = models.ForeignKey(Profile, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(300)])
    scoring = models.CharField(max_length=50, choices=SCORING_CHOICES)
    score_type = models.CharField(max_length=50, choices=PIECE_TYPE_CHOICES)
    genre_1 = models.CharField(max_length=50, choices=GENRE_CHOICES)
    genre_2 = models.CharField(max_length=50, choices=GENRE_CHOICES, blank=True)
    published_key = models.CharField(max_length=50, choices=KEY_CHOICES)
    file = models.FileField(upload_to='media/scores/files/', validators=[validate_pdf])
    youtube_video_link = models.URLField(max_length=200, blank=True, null=True)
    publication_date = models.DateField(auto_now_add=True)
    pages = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], blank=True, null=True)
    cover = models.FileField(upload_to='media/scores/covers', blank=True, null=True)
    # review

    def __str__(self):
        return f'{self.title} By {self.arranger}'

    def detailed_str(self):
        return f'sheetmusic with pk: {self.pk}\n' \
               f'title: {self.title}\n' \
               f'arranger: {self.arranger.user.username}\n' \
               f'price: {self.price}€\n' \
               f'scoring: {self.scoring}\n' \
               f'score type: {self.score_type}\n' \
               f'genre: {self.genre_1} {self.genre_2}\n' \
               f'key: {self.published_key}\n' \
               f'pages: {self.pages}\n'

    def set_pages_number(self):
        try:
            with open(self.file.path, 'rb') as pdf:
                reader = PyPDF2.PdfReader(pdf)
                self.pages = len(reader.pages)
                self.save()
                print(f'numero di pagine salvato: {self.pages}')
        except Exception as e:
            print(f'Errore nel leggere il file PDF: {e}')

    def set_pdf_first_page_as_cover(self):
        if not self.file: return None

        try:
            covers_dir = os.path.join(BASE_DIR, 'media', 'scores', 'covers')

            os.makedirs(covers_dir, exist_ok=True)

            out_image_path = os.path.join(covers_dir, f'{self.pk}_cover.jpg')

            with fitz.open(self.file.path) as pdf_document:
                first_page = pdf_document[0]
                pix = first_page.get_pixmap(dpi=140)
                pix.save(out_image_path)

            self.cover.name = f'media/scores/covers/{self.pk}_cover.jpg'
            self.save()
            print(f'copertina generata e salvata: {self.cover.name}')

        except Exception as e:
            print(f'Errore nel generare la copertina: {e}')

    def get_youtube_video_id_from_link(self):
        if not self.youtube_video_link: return None
        query = urlparse(self.youtube_video_link)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                return parse_qs(query.query).get('v', [None])[0]
            if query.path.startswith('/embed/'):
                return query.path.split('/')[2]
        return None



class Copy(models.Model):
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now=False, auto_now_add=True)
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(30)])
