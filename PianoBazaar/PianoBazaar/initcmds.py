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
            'username': 'Bach',
            'password': 'Bach1234',
            'email': 'bach@gmail.com',
            'first_name': 'Johann Sebastian',
            'last_name': 'Bach',
            'bio': '"I am Johann Sebastian Bach, a humble servant of music and faith.'
                   ' Born in Eisenach in 1685, I have devoted my life to composing and performing for the glory of God.'
                   ' Through my works, I seek to unite technical mastery with spiritual depth, offering music that speaks to both the mind and the soul."',
            'mantra': 'Music\'s only purpose should be the glory of God and the refreshment of the soul.',
            'birth_date': date(1685, 3, 31),
            'profile_image': 'media/profiles/profile_imgs/Bach.jpeg',
            'youtube_account_id': '',
            'instagram_account_id': '',
            'x_account_id': '',
        },
        {
            'username': 'ScottJoplin',
            'password': 'ScottJoplin1234',
            'email': 'scott@gmail.com',
            'first_name': 'Scott',
            'last_name': 'Joplin',
            'bio': '"I am Scott Joplin, born in 1868 in Texarkana, Texas, a composer and pianist who brought the rhythms of ragtime into the hearts of America.'
                   ' Known as the \'King of Ragtime,\' I dedicated my life to crafting music that blended joyful syncopation with deep, emotional expression.',
            'mantra': 'I want to make music that will be remembered.',
            'birth_date': date(1867, 1, 1),
            'profile_image': 'media/profiles/profile_imgs/Scott-Joplin.jpg',
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
            'profile_image': 'media/profiles/profile_imgs/dripping-cat.jpg',
            'youtube_account_id': 'DLMusicPiano',
            'instagram_account_id': 'davidelasagni',
            'x_account_id': 'yomii_piano',
        },
        {
            'username': 'Fabrizio',
            'password': 'Fabrizio1234',
            'email': 'fabrizio@gmail.com',
            'first_name': 'Fabrizio',
            'last_name': 'Pesce',
            'bio': 'In my free time i like to swim and play some piano.',
            'mantra': 'The best gift we have, is tomorrow.',
            'birth_date': date(2004, 1, 13),
            'profile_image': 'media/profiles/profile_imgs/axolotl-large-photo.jpg',
            'youtube_account_id': '',
            'instagram_account_id': '',
            'x_account_id': '',
        },
        {
            'username': 'Paolo',
            'password': 'Paolo1234',
            'email': 'paolo@gmail.com',
            'first_name': 'Paolo',
            'last_name': 'Festino',
            'bio': 'In my free time i like to hit the gym, make parties, and play some piano.',
            'mantra': 'Things that look easy, are usually the hardest.',
            'birth_date': date(2003, 9, 1),
            'profile_image': 'media/profiles/profile_imgs/puppy.jpg',
            'youtube_account_id': '',
            'instagram_account_id': '',
            'x_account_id': '',
        },
        {
            'username': 'Giovanni',
            'password': 'Giovanni1234',
            'email': 'giova@gmail.com',
            'first_name': 'Giovanni',
            'last_name': 'Bellescarpe',
            'bio': 'In my free time i like to make remixes, get drunk and play some piano.',
            'mantra': 'Nothing hits hard, like an afro hairstyle.',
            'birth_date': date(2002, 4, 1),
            'profile_image': 'media/profiles/profile_imgs/giovanni-bellescarpe.jpg',
            'youtube_account_id': '',
            'instagram_account_id': '',
            'x_account_id': '',
        },
        {
            'username': 'Luca',
            'password': 'Luca1234',
            'email': 'luca@gmail.com',
            'first_name': 'Luca',
            'last_name': 'Shampini',
            'bio': 'Everybody calls me mask, but you can call me anytime.',
            'mantra': 'Music, i need nothing else.',
            'birth_date': date(2002, 3, 1),
            'profile_image': 'media/profiles/profile_imgs/black-hole-space.jpg',
            'youtube_account_id': '',
            'instagram_account_id': '',
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
            'title': 'Sonata No.8 in C Minor Op.13 "Pathétique"',
            'arranger': Profile.objects.get(user__username='Beethoven'),
            'price': Decimal('11.99'),
            'scoring': 'Piano solo',
            'score_type': 'public domain',
            'genre_1': 'classical',
            'genre_2': '',
            'published_key': 'C minor',
            'file': 'media/scores/files/Beethoven_pathetique_No.8_Op.13.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=qO8yfBLNVjU',
        },
        {
            'title': 'Nocturne in C op.48 No.1',
            'arranger': Profile.objects.get(user__username='Chopin'),
            'price': Decimal('10.99'),
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
            'price': Decimal('10.99'),
            'scoring': 'piano solo',
            'score_type': 'public domain',
            'genre_1': 'classical',
            'genre_2': '',
            'published_key': 'Eb major',
            'file': 'media/scores/files/Nocturne_Op.9_No.2.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=9E6b3swbnWg',
        },
        {
            'title': 'Nocturne in C Sharp Minor No.20',
            'arranger': Profile.objects.get(user__username='Chopin'),
            'price': Decimal('10.99'),
            'scoring': 'piano solo',
            'score_type': 'public domain',
            'genre_1': 'classical',
            'genre_2': '',
            'published_key': 'C# minor',
            'file': 'media/scores/files/Chopin_Nocturne_In_C_Sharp_Minor_No.20.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=s_ST3hzMsVE',
        },
        {
            'title': 'Fantaisie Impromptu, Op.66',
            'arranger': Profile.objects.get(user__username='Chopin'),
            'price': Decimal('10.99'),
            'scoring': 'piano solo',
            'score_type': 'public domain',
            'genre_1': 'classical',
            'genre_2': '',
            'published_key': 'C# minor',
            'file': 'media/scores/files/Chopin_Fantaisie_Impromptu_Op.66.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=B-HosIOod_A',
        },
        {
            'title': 'Revolutionary Etude Op.10 No.12',
            'arranger': Profile.objects.get(user__username='Chopin'),
            'price': Decimal('10.99'),
            'scoring': 'piano solo',
            'score_type': 'public domain',
            'genre_1': 'classical',
            'genre_2': '',
            'published_key': 'C minor',
            'file': 'media/scores/files/Chopin_Revolutionary_Etude_in_C_Minor_Op.10_No.12.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=oIsGKyqEP5M',
        },
        {
            'title': 'Prelude in C Major',
            'arranger': Profile.objects.get(user__username='Bach'),
            'price': Decimal('8.99'),
            'scoring': 'piano solo',
            'score_type': 'public domain',
            'genre_1': 'classical',
            'genre_2': '',
            'published_key': 'C major',
            'file': 'media/scores/files/Bach_Prelude_in_C_Major.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=mKsAypz6Ou8',
        },
        {
            'title': 'Maple Leaf Rag',
            'arranger': Profile.objects.get(user__username='ScottJoplin'),
            'price': Decimal('9.99'),
            'scoring': 'piano solo',
            'score_type': 'public domain',
            'genre_1': 'blues',
            'genre_2': 'jazz',
            'published_key': 'Ab major',
            'file': 'media/scores/files/Scott_Joplin_Maple_Leaf_Rag.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=bCxLAr_bwpA',
        },
        {
            'title': 'The Entertainer',
            'arranger': Profile.objects.get(user__username='ScottJoplin'),
            'price': Decimal('9.99'),
            'scoring': 'piano solo',
            'score_type': 'public domain',
            'genre_1': 'blues',
            'genre_2': 'jazz',
            'published_key': 'C major',
            'file': 'media/scores/files/Scott_Joplin_The_Entertainer.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=t9gzZJ344Co',
        },
        {
            'title': 'Elite Syncopations',
            'arranger': Profile.objects.get(user__username='ScottJoplin'),
            'price': Decimal('9.99'),
            'scoring': 'piano solo',
            'score_type': 'public domain',
            'genre_1': 'blues',
            'genre_2': 'jazz',
            'published_key': 'F major',
            'file': 'media/scores/files/Scott_Joplin_Elite_Syncopations.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=l_dZWHm7I78',
        },
        {
            'title': 'Felicity Rag',
            'arranger': Profile.objects.get(user__username='ScottJoplin'),
            'price': Decimal('9.99'),
            'scoring': 'piano solo',
            'score_type': 'public domain',
            'genre_1': 'blues',
            'genre_2': 'jazz',
            'published_key': 'C major',
            'file': 'media/scores/files/Scott_Joplin_Scott_Hayden_felicity_Rag.pdf',
            'youtube_video_link': 'https://www.youtube.com/watch?v=0K28yCQWn5w',
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


    # p1=Profile.objects.get(user__username='Lasa')
    # p1.purchased_scores.add(Score.objects.get(title='Maple Leaf Rag'))
    # p1.purchased_scores.add(Score.objects.get(title='The Entertainer'))
    # p1.purchased_scores.add(Score.objects.get(title='Revolutionary Etude Op.10 No.12'))
    # p1.purchased_scores.add(Score.objects.get(title='Moonlight Sonata No.14'))
    # p1.purchased_scores.add(Score.objects.get(title='Nocturne in C op.48 No.1'))
    #
    # p2=Profile.objects.get(user__username='Chopin')
    # p2.purchased_scores.add(Score.objects.get(title='We Found Love X Stereo Love'))
    # p2.purchased_scores.add(Score.objects.get(title='Sonata No.8 in C Minor Op.13 "Pathétique"'))
    # p2.purchased_scores.add(Score.objects.get(title='Elite Syncopations'))
    #
    # p3=Profile.objects.get(user__username='Paolo')
    # p3.purchased_scores.add(Score.objects.get(title='Felicity Rag'))
    # p3.purchased_scores.add(Score.objects.get(title='Nocturne op.9 No.2'))
    # p3.purchased_scores.add(Score.objects.get(title='Prelude in C Major'))
    #
    # p4=Profile.objects.get(user__username='Giovanni')
    # p4.purchased_scores.add(Score.objects.get(title='The Entertainer'))
    # p4.purchased_scores.add(Score.objects.get(title='Nocturne op.9 No.2'))
    # p4.purchased_scores.add(Score.objects.get(title='Fantaisie Impromptu, Op.66'))
    # p4.purchased_scores.add(Score.objects.get(title='Sonata No.8 in C Minor Op.13 "Pathétique"'))
    #
    # p5=Profile.objects.get(user__username='Luca')
    # p5.purchased_scores.add(Score.objects.get(title='Fur Elise'))
    # p5.purchased_scores.add(Score.objects.get(title='Elite Syncopations'))
    # p5.purchased_scores.add(Score.objects.get(title='Nocturne op.9 No.2'))
    #
    # p6=Profile.objects.get(user__username='Beethoven')
    # p6.purchased_scores.add(Score.objects.get(title='Nocturne in C Sharp Minor No.20'))


