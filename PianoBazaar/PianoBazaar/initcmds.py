import os
from datetime import datetime, date
from decimal import Decimal

from django.conf.global_settings import MEDIA_URL
from django.contrib.auth.models import User

from sheetmusic.models import Score, Profile, Copy

def erase_db():
    print("Erasing DB")
    Score.objects.all().delete()
    Copy.objects.all().delete()
    User.objects.all().delete()
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

    scores_data = [
        {
            'title': 'Moonlight Sonata No.14',
            'arranger': 'Beethoven',
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
            'arranger': 'Beethoven',
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
            'arranger': 'Chopin',
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
            'arranger': 'Chopin',
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
            'arranger': 'Lasa',
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

    for user_data in users_data:
        username = user_data['username']
        password = user_data['password']
        email = user_data['email']
        first_name = user_data['first_name']
        last_name = user_data['last_name']
        bio = user_data['bio']
        mantra = user_data['mantra']
        birth_date = user_data['birth_date']
        profile_image = user_data['profile_image']
        youtube_account_id = user_data['youtube_account_id']
        instagram_account_id = user_data['instagram_account_id']
        x_account_id = user_data['x_account_id']


        print('provo a creare ' + username)
        try:
            user = User.objects.get(username=username)
            print('user ' + username + ' already exists!')
            continue
        except User.DoesNotExist:
            print('user ' + username + ' does not exist!')


        user, created = User.objects.get_or_create(username=username, email=email, first_name=first_name, last_name=last_name,)
        if created:
            print('user ' + username + ' created!')
            user.set_password(password)
            print('password set')
            user.save()
            print('user saved')
        else:
            print('FALLITO A CREARE USER ORCOKAN!')

        print("provo a creare il profilo")
        print(birth_date)
        profile, created = Profile.objects.get_or_create(user=user, bio=bio, mantra=mantra, birth_date=birth_date, profile_image=profile_image,
                                                         youtube_account_id=youtube_account_id, instagram_account_id=instagram_account_id, x_account_id=x_account_id,
                                                         )
        if created:
            print('profile created!')
            profile.save()
            print("sto per stampare il profilo creato")
            print(profile)
        else:
            print('FALLITO A CREARE PROFILO ORCOKAN!')


    for score_data in scores_data:
        #Score.objects.get_or_create(**score_data)
        title = score_data['title']
        arranger = score_data['arranger']
        price = score_data['price']
        scoring = score_data['scoring']
        score_type = score_data['score_type']
        genre_1 = score_data['genre_1']
        genre_2 = score_data['genre_2']
        published_key = score_data['published_key']
        file = score_data['file']
        youtube_video_link = score_data['youtube_video_link']

        print("\nprovo a creare lo spartito intitolato " +title)
        score, created = Score.objects.get_or_create(title=title,
                                                     arranger=Profile.objects.get(user__username=arranger),
                                                     price=price,
                                                     scoring=scoring,
                                                     score_type=score_type,
                                                     genre_1=genre_1, genre_2=genre_2,
                                                     published_key=published_key,
                                                     file=file,
                                                     youtube_video_link=youtube_video_link)
        if created:
            score.save()
            print(score)
        else:
            print('FALLITO A CREARE SPARTITO ORCOKAN!')

    print("Success!, DB initialized")



