from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from PianoBazaar.forms import ProfileCreationForm, UserCreateForm
from sheetmusic.models import Profile


def home(request):
    return render(request, template_name='home.html')

class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = "user_create.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        user = form.save()
        self.request.session['new_user_id'] = user.id
        return super().form_valid(form)

class ProfileCreateView(CreateView):
    form_class = ProfileCreationForm
    template_name = "profile_create.html"
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        # Assicurati che ci sia un utente salvato in sessione
        if 'new_user_id' not in request.session:
            return redirect('register')  # Reindirizza alla registrazione se non c'è un utente
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form): # Serve per aggiungere azioni aggiuntive post form-validation prima della reindirizzazione. Questo approccio è più chiaro, segue le best practices di Django ed è facile da mantenere
        # Recupera l'utente dalla sessione
        user_id = self.request.session.pop('new_user_id')  # Rimuovi l'ID dalla sessione
        user = User.objects.get(id=user_id)
        form.instance.user = user
        return super().form_valid(form)


