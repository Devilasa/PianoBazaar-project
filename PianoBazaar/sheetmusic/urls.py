from django.urls import re_path, path
from django.views.generic import detail

from .views import *

app_name = 'sheetmusic'

urlpatterns = [
    # re_path(r'^$|^/$|^home/$', ScoreList.as_view(), name='home'),
    path('', ScoreList.as_view(), name='home'),
    path('<str:s_string>', SearchScore.as_view(), name='search_score'),
    path('score-upload/', ScoreCreate.as_view(), name='score_upload'),
    path('score-delete/<score_pk>', score_delete, name='score_delete'),
    path('add-liked-score/<score_pk>', like_score, name='add_liked_score'),
    path('add-score-to-shopping-cart/<score_pk>', manage_score_for_shopping_cart, name='add_score_to_shopping_cart'),
    path('arranger/<pk>/view-shopping-cart/', ArrangerViewShoppingCart.as_view(), name='view_shopping_cart'),
    path('detail/<pk>/', ScoreDetail.as_view(), name='detail'),
    path('visualize/<pk>/', ScoreVisualize.as_view(), name='visualize_score'),
    path('profiles/', ArrangerList.as_view(), name= 'profiles'),
    path('profiles/<str:s_string>', SearchProfile.as_view(), name= 'search_profile'),
    path('update-profile/<pk>/', ProfileUpdate.as_view(), name='update_profile'),
    path('arranger/<pk>/', ArrangerDetail.as_view(), name='arranger'),
    path('arranger/<pk>/liked-scores/', ArrangerDetailLikedScores.as_view(), name='arranger_liked_scores'),
    path('arranger/<pk>/purchased-scores/', ArrangerDetailPurchasedScores.as_view(), name='arranger_purchased_scores'),
    path('profile/<pk>/sales-insights/', SalesInsights.as_view(), name='sales_insights'),
    path('score/<score_pk>/pre-checkout/', pre_checkout, name='pre_checkout'),
    path('user/<pk>/checkout/', Checkout.as_view(), name='checkout'),

]