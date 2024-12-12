from datetime import datetime, date
from decimal import Decimal

from django.contrib.auth.models import User

from sheetmusic.models import Score, Profile, Copy

def erase_db():
    print("Erasing DB")
    Score.objects.all().delete()
    Copy.objects.all().delete()
    User.objects.all().delete()
    Profile.objects.all().delete()

def init_db():
    print("Initializing DB")

    if len(Score.objects.all()) > 0: return

    users_data = [
         {
            'username': 'Gianni',
            'password': 'gianni1234',
            'email': 'gianni@gmail.com',
            'first_name': 'gianni',
            'last_name': 'giovanni',
            'bio': 'the gianni guy',
            'birth_date': date(1990, 1, 1)
        },
        {
            'username': 'Pippo',
            'password': 'pippo1234',
            'email': 'pippo@gmail.com',
            'first_name': 'pippo',
            'last_name': 'filippo',
            'bio': 'the pippo guy',
            'birth_date': date(2001, 2, 2)
        }
    ]

    scores_data = [
        {
            'title': 'summer',
            'arranger': 'Pippo',
            'price': Decimal('9.99'),
            'scoring': 'piano solo',
            'score_type': 'creation',
            'genre_1': 'blues',
            'genre_2': '',
            'published_key': 'B major',
            'file': '',
            'youtube_video_link': '',
        },
        {
            'title': 'autumn',
            'arranger': 'Pippo',
            'price': Decimal('5'),
            'scoring': 'piano solo',
            'score_type': 'creation',
            'genre_1': 'blues',
            'genre_2': 'epic',
            'published_key': 'C minor',
            'pages': 2,
            'file': '',
            'youtube_video_link': '',
        },
        {
            'title': 'winter',
            'arranger': 'Pippo',
            'price': Decimal('10.00'),
            'scoring': 'piano solo',
            'score_type': 'mash-up',
            'genre_1': 'experimental',
            'genre_2': 'relax',
            'published_key': 'C major',
            'pages': 6,
            'file': '',
            'youtube_video_link': '',
        },
        {
            'title': 'spring',
            'arranger': 'Gianni',
            'price': Decimal('20.99'),
            'scoring': 'piano solo',
            'score_type': 'cover',
            'genre_1': 'classical',
            'genre_2': '',
            'published_key': 'E major',
            'pages': 10,
            'file': '',
            'youtube_video_link': '',
        },
    ]

    for user_data in users_data:
        username = user_data['username']
        password = user_data['password']
        email = user_data['email']
        first_name = user_data['first_name']
        last_name = user_data['last_name']
        bio = user_data['bio']
        birth_date = user_data['birth_date']


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
        profile, created = Profile.objects.get_or_create(user=user, bio=bio, birth_date=birth_date)
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



