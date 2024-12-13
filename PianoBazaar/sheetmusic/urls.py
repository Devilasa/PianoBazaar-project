from django.urls import re_path, path
from .views import *

app_name = 'sheetmusic'

urlpatterns = [
    re_path(r'^$|^/$|^home/$', ScoreList.as_view(), name='home'),
    # path('sheet_list/', ScoreList.as_view(), name='sheet_list'),
    path('create_sheet/', CreateSheetMusic.as_view(), name='create_sheet')

]