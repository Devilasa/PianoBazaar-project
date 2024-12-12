import os.path
import PyPDF2
import fitz

from PyPDF2 import PdfReader
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
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    purchased_scores = models.ManyToManyField('Score', through='Copy')

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}'


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
    arranger = models.ForeignKey(Profile, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(300)])
    scoring = models.CharField(max_length=50, choices=SCORING_CHOICES)
    score_type = models.CharField(max_length=50, choices=PIECE_TYPE_CHOICES)
    genre_1 = models.CharField(max_length=50, choices=GENRE_CHOICES)
    genre_2 = models.CharField(max_length=50, choices=GENRE_CHOICES, blank=True)
    published_key = models.CharField(max_length=50, choices=KEY_CHOICES)
    file = models.FileField(upload_to='media/scores/files/', validators=[validate_pdf], null=True) # lo metteremo obbligatorio ovviamente, per rafforzare il controllo librerie mimetypes o magic
    youtube_video_link = models.CharField(max_length=50, blank=True)  # ricordati di fare l'estrazione
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
                print(type(first_page))
                pix = first_page.get_pixmap(dpi=200)
                pix.save(out_image_path)

            self.cover.name = f'scores/covers/{self.pk}_cover.jpg'
            self.save()
            print(f'copertina generata e salvata: {self.cover.name}')

        except Exception as e:
            print(f'Errore nel generare la copertina: {e}')





class Copy(models.Model):
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now=False, auto_now_add=True)
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(30)])
