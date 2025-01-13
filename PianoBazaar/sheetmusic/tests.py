from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.db.models.signals import post_save
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from sheetmusic.models import Profile, Score, Copy, BillingProfile
from sheetmusic.signals import add_login_message, generate_cover_on_save

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


class PermissionTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="user1_test")
        self.user2 = User.objects.create(username="user2_test")
        self.user3 = User.objects.create(username="user3_test")
        self.user4_admin = User.objects.create(username="user4_admin_test", is_staff=True)
        self.user5_admin = User.objects.create(username="user5_admin_test", is_staff=True)
        self.superuser = User.objects.create(username="superuser_test", is_superuser=True, is_staff=True)

        self.user1.set_password("<PASSWORD>")
        self.user1.save()
        self.user2.set_password("<PASSWORD>")
        self.user2.save()
        self.user3.set_password("<PASSWORD>")
        self.user3.save()
        self.user4_admin.set_password("<PASSWORD>")
        self.user4_admin.save()
        self.user5_admin.set_password("<PASSWORD>")
        self.user5_admin.save()
        self.superuser.set_password("<PASSWORD>")
        self.superuser.save()

        self.arranger1 = Profile.objects.create(user=self.user1)
        self.arranger2 = Profile.objects.create(user=self.user2)
        self.arranger3 = Profile.objects.create(user=self.user3)
        self.arranger4_admin = Profile.objects.create(user=self.user4_admin)
        self.arranger5_admin = Profile.objects.create(user=self.user5_admin)

        self.b_profile1 = BillingProfile.objects.create(user=self.user1)
        self.b_profile2 = BillingProfile.objects.create(user=self.user2)
        self.b_profile3 = BillingProfile.objects.create(user=self.user3)
        self.b_profile4_admin = BillingProfile.objects.create(user=self.user4_admin)
        self.b_profile5_admin = BillingProfile.objects.create(user=self.user5_admin)

        self.score1 = Score.objects.create(title = "score test1",arranger = self.arranger1, price = 20.00, scoring = "Piano solo",
                                           score_type = "Original Composition", genre_1 = "Pop", published_key = "C Major",
                                           file='media/tests/scores/Scott_Joplin_Maple_Leaf_Rag.pdf'
                                           )
        self.score2 = Score.objects.create(title="score test2", arranger=self.arranger1, price=20.00, scoring="Piano solo",
                                           score_type="Original Composition", genre_1="Pop", published_key="C Major",
                                           file='media/tests/scores/Scott_Joplin_Maple_Leaf_Rag.pdf'
                                           )
        self.score3 = Score.objects.create(title="score test3", arranger=self.arranger1, price=20.00, scoring="Piano solo",
                                           score_type="Original Composition", genre_1="Pop", published_key="C Major",
                                           file='media/tests/scores/Scott_Joplin_Maple_Leaf_Rag.pdf'
                                           )
        self.score4 = Score.objects.create(title="score test4", arranger=self.arranger2, price=20.00, scoring="Piano solo",
                                           score_type="Original Composition", genre_1="Pop", published_key="C Major",
                                           file='media/tests/scores/Scott_Joplin_Maple_Leaf_Rag.pdf'
                                           )
        self.score5 = Score.objects.create(title="score test5", arranger=self.arranger2, price=20.00, scoring="Piano solo",
                                           score_type="Original Composition", genre_1="Pop", published_key="C Major",
                                           file='media/tests/scores/Scott_Joplin_Maple_Leaf_Rag.pdf'
                                           )
        self.score6 = Score.objects.create(title="score test6", arranger=self.arranger3, price=20.00, scoring="Piano solo",
                                           score_type="Original Composition", genre_1="Pop", published_key="C Major",
                                           file='media/tests/scores/Scott_Joplin_Maple_Leaf_Rag.pdf'
                                           )
        self.score7 = Score.objects.create(title="score test7", arranger=self.arranger4_admin, price=20.00, scoring="Piano solo",
                                           score_type="Original Composition", genre_1="Pop", published_key="C Major",
                                           file='media/tests/scores/Scott_Joplin_Maple_Leaf_Rag.pdf'
                                           )

        self.score4_copy = Copy.objects.create(score=self.score4, buyer=self.arranger1)

        user_logged_in.disconnect(add_login_message)
        post_save.disconnect(generate_cover_on_save, sender=Score)

    def tearDown(self):
        user_logged_in.connect(add_login_message)
        post_save.connect(generate_cover_on_save, sender=Score)



    def test_normal_user_score_visualization(self):
        self.client.login(username="user1_test", password="<PASSWORD>")

        response = self.client.get(reverse('sheetmusic:visualize_score', kwargs={'pk': self.score1.pk}))
        self.assertEqual(response.status_code, 200)  # Success, user can visualize his own scores.

        response = self.client.get(reverse('sheetmusic:visualize_score', kwargs={'pk': self.score4.pk}))
        self.assertEqual(response.status_code, 200)  # Success, user can visualize a purchased score.

        response = self.client.get(reverse('sheetmusic:visualize_score', kwargs={'pk': self.score5.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden, user can't visualize scores he didn't buy.


    def test_user_is_admin_score_visualization(self):
        self.client.login(username="user4_admin_test", password="<PASSWORD>")

        response = self.client.get(reverse('sheetmusic:visualize_score', kwargs={'pk': self.score1.pk}))
        self.assertEqual(response.status_code, 200) # Success, admin can visualize all the scores.


    def test_superuser_score_visualization(self):
        self.client.login(username="superuser_test", password="<PASSWORD>")

        response = self.client.get(reverse('sheetmusic:visualize_score', kwargs={'pk': self.score1.pk}))
        self.assertEqual(response.status_code, 200) # Success, superuser can visualize all the scores.



    def test_normal_user_score_deletion(self):
        self.client.login(username="user1_test", password="<PASSWORD>")

        response = self.client.post(reverse('sheetmusic:score_delete', kwargs={'score_pk': self.score1.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect, the expected behaviour when the score gets deleted. User is the owner.
        with self.assertRaises(Score.DoesNotExist):
            Score.objects.get(pk=self.score1.pk)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "The score has been deleted.")

        response = self.client.get(reverse('sheetmusic:score_delete', kwargs={'score_pk': self.score4.pk}))
        self.assertEqual(response.status_code, 403) # 403 forbidden, user is not the owner.


    def test_user_is_admin_score_deletion(self):
        self.client.login(username="user4_admin_test", password="<PASSWORD>")

        response = self.client.post(reverse('sheetmusic:score_delete', kwargs={'score_pk': self.score2.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect, expected behaviour, admin can delete other user scores.
        with self.assertRaises(Score.DoesNotExist):
            Score.objects.get(pk=self.score2.pk)


    def test_superuser_score_deletion(self):
        self.client.login(username="superuser_test", password="<PASSWORD>")

        response = self.client.post(reverse('sheetmusic:score_delete', kwargs={'score_pk': self.score3.pk}))
        self.assertEqual(response.status_code, 302)  # Success, superuser can delete other user scores.
        with self.assertRaises(Score.DoesNotExist):
            Score.objects.get(pk=self.score3.pk)


    def test_normal_user_profile_deletion(self):
        self.client.login(username="user1_test", password="<PASSWORD>")

        profiles_count = Profile.objects.all().count()
        response = self.client.get(reverse('sheetmusic:profile_delete', kwargs={'profile_pk': self.arranger2.pk}))
        self.assertEqual(response.status_code, 302)  # Redirected to the staff member login page, only admin profiles can delete profiles.
        self.assertEqual(profiles_count, Profile.objects.all().count())


    def test_user_is_admin_profile_deletion(self):
        self.client.login(username="user4_admin_test", password="<PASSWORD>")

        response = self.client.post(reverse('sheetmusic:profile_delete', kwargs={'profile_pk': self.arranger2.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect, expected behaviour, admin can delete other users profiles.
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(pk=self.arranger2.pk)

        response = self.client.get(reverse('sheetmusic:profile_delete', kwargs={'profile_pk': self.arranger5_admin.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden, admin can't delete other admins profiles.


    def test_superuser_profile_deletion(self):
        self.client.login(username="superuser_test", password="<PASSWORD>")

        response = self.client.post(reverse('sheetmusic:profile_delete', kwargs={'profile_pk': self.arranger5_admin.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect, expected behaviour, superuser can delete admins profiles.
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(pk=self.arranger5_admin.pk)

