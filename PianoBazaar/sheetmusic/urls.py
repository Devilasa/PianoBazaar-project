from django.urls import re_path, path
from django.views.generic import detail

from .views import *

app_name = 'sheetmusic'

urlpatterns = [
    re_path(r'^$|^/$|^home/$', ScoreList.as_view(), name='home'),
    path('score-upload/', ScoreCreate.as_view(), name='score_upload'),
    path('add-liked-score/<score_pk>', like_score, name='add_liked_score'),
    path('add-score-to-shopping-cart/<score_pk>', manage_score_for_shopping_cart, name='add_score_to_shopping_cart'),
    path('detail/<pk>/', ScoreDetail.as_view(), name='detail'),
    path('visualize/<pk>/', ScoreVisualize.as_view(), name='visualize_score'),
    path('profiles/', ArrangerList.as_view(), name= 'profiles'),
    path('update-profile/<pk>/', ProfileUpdate.as_view(), name='update_profile'),
    path('arranger/<pk>/', ArrangerDetail.as_view(), name='arranger'),
    path('arranger/<pk>/liked-scores/', ArrangerDetailLikedScores.as_view(), name='arranger_liked_scores'),
    path('arranger/<pk>/purchased-scores/', ArrangerDetailPurchasedScores.as_view(), name='arranger_purchased_scores'),
    path('score/<score_pk>/pre-checkout/', pre_checkout, name='pre_checkout'),
    path('user/<pk>/checkout/', Checkout.as_view(), name='checkout'),

]