from django.urls import re_path, path
from django.views.generic import detail

from .views import *

app_name = 'sheetmusic'

urlpatterns = [
    # re_path(r'^$|^/$|^home/$', ScoreList.as_view(), name='home'),
    path('', ScoreList.as_view(), name='home'),
    path('<str:s_string>', SearchScore.as_view(), name='search_score'),
    path('score-upload/', ScoreCreate.as_view(), name='score_upload'),
    path('score-delete/<score_pk>/', score_delete, name='score_delete'),
    path('genre/<str:genre>/', FilterScoreOnGenre.as_view(), name='filter_genre'),
    path('toggle-like/<score_pk>/', toggle_like, name='toggle_like'),
    path('toggle-score-in-shopping-cart/<score_pk>/', toggle_score_in_shopping_cart, name='toggle_score_in_shopping_cart'),
    path('remove-score-from-shopping-cart/<score_pk>/', remove_score_from_shopping_cart, name='remove_score_from_shopping_cart'),
    path('arranger/<pk>/view-shopping-cart/', ArrangerViewShoppingCart.as_view(), name='view_shopping_cart'),
    path('detail/<pk>/', ScoreDetail.as_view(), name='detail'),
    path('visualize/<pk>/', ScoreVisualize.as_view(), name='visualize_score'),
    path('profiles/', ArrangerList.as_view(), name= 'profiles'),
    path('profiles/<str:s_string>', SearchProfile.as_view(), name= 'search_profile'),
    path('update-profile/<pk>/', ProfileUpdate.as_view(), name='update_profile'),
    path('profile-delete/<profile_pk>/', profile_delete, name='profile_delete'),
    path('arranger/<pk>/', ArrangerDetail.as_view(), name='arranger'),
    path('arranger/<pk>/liked-scores/', ArrangerDetailLikedScores.as_view(), name='arranger_liked_scores'),
    path('arranger/<pk>/purchased-scores/', ArrangerDetailPurchasedScores.as_view(), name='arranger_purchased_scores'),
    path('profile/<pk>/sales-insights/', SalesInsights.as_view(), name='sales_insights'),
    path('score/<score_pk>/pre-checkout/', pre_checkout, name='pre_checkout'),
    path('user/<pk>/checkout/', Checkout.as_view(), name='checkout'),

]