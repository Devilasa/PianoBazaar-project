from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from PianoBazaar.forms import ProfileCreationForm, UserCreateForm
from sheetmusic.models import Score, BillingProfile


def home(request):
    return render(request, template_name='home.html')

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sheetmusic:home')

    previous_url = request.META.get('HTTP_REFERER', '/sheetmusic/')
    request.session['logout_modal'] = 'show'
    return redirect(previous_url)

class LoginViewCustom(LoginView):
    def get(self, request, *args, **kwargs):
        if 'next' in request.GET:
            next_url = request.GET['next'].split('/')[-1]
            messages.warning(request, f'You need to login in order to access {next_url} page', extra_tags='alert-danger')
        return super().get(request, *args, **kwargs)


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = "registration/user_create.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        user = form.save()
        self.request.session['new_user_id'] = user.id
        return super().form_valid(form)

class ProfileCreateView(SuccessMessageMixin, CreateView):
    form_class = ProfileCreationForm
    template_name = "registration/profile_create.html"
    success_url = reverse_lazy("login")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.created_user = None

    def dispatch(self, request, *args, **kwargs):
        # Assicurati che ci sia un utente salvato in sessione
        if 'new_user_id' not in request.session:
            return redirect('register')  # Reindirizza alla registrazione se non c'è un utente
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form): # Serve per aggiungere azioni aggiuntive post form-validation prima della reindirizzazione. Questo approccio è più chiaro, segue le best practices di Django ed è facile da mantenere
        user_id = self.request.session.pop('new_user_id')  # Rimuovi l'ID dalla sessione
        user = User.objects.get(id=user_id)
        form.instance.user = user
        self.created_user = user
        BillingProfile.objects.get_or_create(user=user)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return f"{self.created_user.username}'s profile was successfully created."



