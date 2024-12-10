from django.urls import re_path, path
from .views import *

app_name = 'sheetmusic'

urlpatterns = [
    re_path(r'^$|^/$|^home/$', sheetmusic_home, name='home'),

    path('create_sheet/', CreateSheetMusic.as_view(), name='create_sheet')

]