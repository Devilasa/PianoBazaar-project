"""
URL configuration for PianoBazaar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import profile

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import settings
from .initcmds import init_db, erase_db
from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$|^/$|^home/$', home, name='home'),
    path('sheetmusic/', include('sheetmusic.urls')),

    path("register/", UserCreateView.as_view(), name="register"),
    path("profile/", ProfileCreateView.as_view(), name="profile"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

erase_db()
init_db()
