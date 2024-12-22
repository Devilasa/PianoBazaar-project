from django.urls import re_path, path
from django.views.generic import detail

from .views import *

app_name = 'sheetmusic'

urlpatterns = [
    re_path(r'^$|^/$|^home/$', ScoreList.as_view(), name='home'),
    path('create-sheet/', CreateSheetMusic.as_view(), name='create_sheet'),
    path('detail/<pk>/', ScoreDetail.as_view(), name='detail'),
    path('arranger/<pk>/', ArrangerDetail.as_view(), name='arranger'),
    path('arranger/<pk>/liked-scores/', ArrangerDetailLikedScores.as_view(), name='arranger_liked_scores'),
    path('arranger/<pk>/purchased-scores/', ArrangerDetailPurchasedScores.as_view(), name='arranger_purchased_scores'),

]