import os
from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User

from sheetmusic.models import Score, Profile, Copy, BillingProfile


def erase_db():
    print("Erasing DB")
    Score.objects.all().delete()
    Copy.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    Profile.objects.all().delete()
    for cover_jpg in os.listdir('media/scores/covers/'):
        target_file = os.path.join('media/scores/covers/', cover_jpg)
        os.remove(target_file)

def init_db():
    print("Initializing DB")

    if len(Score.objects.all()) > 0: return

    users_data = [
         {
            'username': 'Beethoven',
            'password': 'Beethoven1234',
            'email': 'beethoven@gmail.com',
            'first_name': 'Ludwig',
            'last_name': 'van Beethoven',
            'bio': 'I\'m german composer and pianist, a pivotal figure in classical music. Despite losing my hearing, i created iconic works like the Ninth Symphony and Moonlight Sonata, bridging Classical and Romantic styles.',
            'mantra': 'Where words fail...music speaks',
            'birth_date': date(1770, 12, 16),
            'profile_image': 'media/profiles/profile_imgs/Beethoven.jpg',
            'youtube_account_id': '',
            'instagram_account_id': '',
            'x_account_id': '',
        },
        {
            'username': 'Chopin',
            'password': 'Chopin1234',
            'email': 'chopin@gmail.com',
            'first_name': 'Fryderyk',
            'last_name': 'Chopin',
            'bio': 'I\'m a polish composer and virtuoso pianist, celebrated for my poetic and technically demanding piano works, including Nocturnes, Preludes, and Mazurkas, defining Romantic piano music.',
            'mantra': 'Simplicity is the highest goal, achievable when you have overcome all difficulties',
            'birth_date': date(1810, 3, 1),
            'profile_image': 'media/profiles/profile_imgs/Chopin.jpg',
            'youtube_account_id': '',
            'instagram_account_id': '',
            'x_account_id': '',
        },
        {
            'username': 'Lasa',
            'password': 'Lasa1234',
            'email': 'lasa@gmail.com',
            'first_name': 'Davide',
            'last_name': 'Lasagni',
            'bio': 'I\'m the creator of this beautiful website and in my free time i\'m also a piano lover!',
            'mantra': 'Convince yourself that you play well, and you will play well.',
            'birth_date': date(2001, 2, 24),
            'profile_image': 'media/profiles/profile_imgs/dripping_cat.jpg',
            'youtube_account_id': 'DLMusicPiano',
            'instagram_account_id': 'davidelasagni',
            'x_account_id': '',
        }
    ]

    for user_data in users_data:
        user_values = {
            'username': user_data['username'],
            'email': user_data['email'],
            'first_name':  user_data['first_name'],
            'last_name': user_data['last_name'],
        }

        profile_values = {
            'user' : '',
            'profile_image': user_data['profile_image'],
            'bio': user_data['bio'],
            'mantra': user_data['mantra'],
            'birth_date': user_data['birth_date'],
            'youtube_account_id': user_data['youtube_account_id'],
            'instagram_account_id': user_data['instagram_account_id'],
            'x_account_id': user_data['x_account_id'],
        }

        user, created = User.objects.get_or_create(**user_values)
        if created:
            print(f'user {user.username} created!')
            user.set_password(user_data['password'])
            user.save()
        else:
            print(f'l\'utente {user.username} already exists!')
        profile_values['user'] = user

        profile, created = Profile.objects.get_or_create(**profile_values)
        if created:
            print(f'profile {user.username} created!')
        else:
            print(f'profile {user.username} already exists!')

        BillingProfile.objects.create(user=user)

    scores_data = [
        {
            'title': 'Moonlight Sonata No.14',
            'arranger': Profile.objects.get(user__username='Beethoven'),
            'price': Decimal('19.99'),
            'scoring': 'piano solo',
            'score_type': 'public domain',
            'genre_1': 'classical',
            'genre_2': '',
            'published_key': 'C# minor',
            'file': 'media/scores/files/Beethoven_Moonlight_Sonata_No.14.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=ITidiBe-0T0',
        },
        {
            'title': 'Fur Elise',
            'arranger': Profile.objects.get(user__username='Beethoven'),
            'price': Decimal('11.99'),
            'scoring': 'Piano solo',
            'score_type': 'public domain',
            'genre_1': 'classical',
            'genre_2': '',
            'published_key': 'A minor',
            'file': 'media/scores/files/Beethoven_fur_Elise_WoO59.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=s71I_EWJk7I',
        },
        {
            'title': 'Nocturne in C op.48 No.1',
            'arranger': Profile.objects.get(user__username='Chopin'),
            'price': Decimal('16.99'),
            'scoring': 'piano solo',
            'score_type': 'public domain',
            'genre_1': 'classical',
            'genre_2': '',
            'published_key': 'C major',
            'file': 'media/scores/files/Nocturne_in_C_Op.48_No.1.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=cpeqVK-FtFA',
        },
        {
            'title': 'Nocturne op.9 No.2',
            'arranger': Profile.objects.get(user__username='Chopin'),
            'price': Decimal('20.99'),
            'scoring': 'piano solo',
            'score_type': 'public domain',
            'genre_1': 'classical',
            'genre_2': '',
            'published_key': 'Eb major',
            'file': 'media/scores/files/Nocturne_Op.9_No.2.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=9E6b3swbnWg',
        },
        {
            'title': 'We Found Love X Stereo Love',
            'arranger': Profile.objects.get(user__username='Lasa'),
            'price': Decimal('5.99'),
            'scoring': 'piano solo',
            'score_type': 'mash-up',
            'genre_1': 'pop',
            'genre_2': 'experimental',
            'published_key': 'C# minor',
            'file': 'media/scores/files/DavideLasagni_WeFoundLoveXStereoLove.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=dD1Y6LiSBVo',
        }
    ]

    for score_data in scores_data:
        score, created = Score.objects.get_or_create(**score_data)
        if created:
            score.save()
            # print(score)
        else:
            print('FALLITO A CREARE SPARTITO ORCOKAN!')

    print("Success!, DB initialized")



