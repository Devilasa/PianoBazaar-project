from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from sheetmusic.models import Profile, Score

"""

Tests executed:

1. youtube link conversion method in Score model
2. total likes calculator method in Score model
3. Score list view working logic

"""

class ScoreModelTest(TestCase):
    def setUp(self):

        self.arranger = Profile.objects.create(user=User.objects.create(username="user test"))
        self.score = Score.objects.create(
            title = "Test Score",
            arranger = self.arranger,
            price = 20.00,
            scoring = "Piano solo",
            score_type = "Original Composition",
            genre_1= "Classical",
            published_key = "C Major",
            youtube_video_link = "https://www.youtube.com/watch?v=dD1Y6LiSBVo",
        )

        self.profile_1 = Profile.objects.create(user=User.objects.create(username="user test 1"))
        self.profile_2 = Profile.objects.create(user=User.objects.create(username="user test 2"))
        self.profile_3 = Profile.objects.create(user=User.objects.create(username="user test 3"))
        self.profile_1.liked_scores.add(self.score)
        self.profile_2.liked_scores.add(self.score)
        self.profile_3.liked_scores.add(self.score)


    def test_get_youtube_video_id_from_link(self):
        # Test the method in expected conditions
        video_id = self.score.get_youtube_video_id_from_link()
        self.assertEqual(video_id, "dD1Y6LiSBVo")

    def test_get_youtube_video_id_from_embed_link(self):
        # Test the method in embed format
        self.score.youtube_video_link = "https://www.youtube.com/embed/dD1Y6LiSBVo"
        video_id = self.score.get_youtube_video_id_from_link()
        print(video_id)
        self.assertEqual(video_id, "dD1Y6LiSBVo")

    def test_get_youtube_video_id_from_short_link(self):
        # Test a link with short format
        self.score.youtube_video_link = "https://youtu.be/dD1Y6LiSBVo"
        video_id = self.score.get_youtube_video_id_from_link()
        self.assertEqual(video_id, "dD1Y6LiSBVo")

    def test_get_youtube_video_id_from_invalid_link(self):
        # Test a non valid link
        self.score.youtube_video_link = "https://example.com/watch?v=dD1Y6LiSBVo"
        video_id = self.score.get_youtube_video_id_from_link()
        self.assertIsNone(video_id)

    def test_total_likes(self):
        total_likes = self.score.total_likes()
        self.assertEqual(total_likes, 3)


class ScoreViewTests(TestCase):


    def setUp(self):
        self.arranger = Profile.objects.create(user=User.objects.create(username="user test"))
        self.score_1 = Score.objects.create(title="Test-Maple Leaf Rag", arranger=self.arranger, price=20.00, scoring="Piano solo", score_type="Public Domain", genre_1='Blues',
                                            genre_2='Jazz', published_key="Ab Major", file='media/tests/scores/Scott_Joplin_Maple_Leaf_Rag.pdf')
        self.score_2 = Score.objects.create(title="Test-The Entertainer", arranger=self.arranger, price=15.00, scoring="Piano solo", score_type="Public Domain", genre_1='Blues',
                                            genre_2='Jazz', published_key="C Major", file='media/tests/scores/Scott_Joplin_The_Entertainer.pdf')


    def test_score_list_template_rendering(self):
        # Checks that we are using the right template
        response = self.client.get(reverse('sheetmusic:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sheetmusic/home.html')

    def test_score_list_content(self):
        # Checks that the scores are in the response
        response = self.client.get(reverse('sheetmusic:home'))
        self.assertContains(response, "Test-Maple Leaf Rag")  # Checks if "Score 1" is in the context
        self.assertContains(response, "Test-The Entertainer")  # Checks if "Score 1" is in the context

    def test_search_redirect(self):
        # Checks the redirect with the parameter 'q'
        response = self.client.get(reverse('sheetmusic:home') + '?q=test_search')
        self.assertEqual(response.status_code, 302)  # State HTTP 302 for redirect
        self.assertRedirects(response, reverse('sheetmusic:search_score', args=['test_search']))