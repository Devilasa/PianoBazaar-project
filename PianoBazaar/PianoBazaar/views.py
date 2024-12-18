from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from PianoBazaar.forms import ProfileCreationForm, UserCreateForm


def home(request):
    return render(request, template_name='home.html')

class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")