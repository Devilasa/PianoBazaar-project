from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from PianoBazaar.forms import ProfileCreationForm, UserCreateForm
from sheetmusic.models import Score, BillingProfile, Profile


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

            referer = request.META.get('HTTP_REFERER', '/')
            referer = urlparse(referer).path

            redirect_url = f'?next={referer}'
            full_redirect_url = f'/login/?next={referer}'

            if full_redirect_url != request.get_full_path():

                # Messaggio di warning
                next_url = request.GET.copy().get('next')
                next_page = next_url.split('/')[2] if '/' in next_url else next_url
                messages.warning(request, f'You need to login in order to {next_page}',
                                 extra_tags='alert-danger')

                return redirect(redirect_url)

        return super().get(request, *args, **kwargs)


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = "registration/user_create.html"

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        profile = Profile.objects.get(user=user)
        self.success_url = reverse_lazy("profile", kwargs={"pk": profile.pk})
        return super().form_valid(form)


class ProfileCreateView(SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = ProfileCreationForm
    template_name = "registration/profile_create.html"
    success_url = reverse_lazy("login")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.created_user = None

    # def dispatch(self, request, *args, **kwargs):
    #     qui posso effettuare dei controlli
    #     return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):  # Serve per aggiungere azioni aggiuntive post form-validation prima della reindirizzazione.
        user = self.object.user  # Questo approccio è più chiaro, segue le best practices di Django ed è facile da mantenere.
        self.created_user = user
        billing_profile = BillingProfile.objects.create(user=user)
        billing_profile.score_receiving_email = user.email
        billing_profile.save()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return f"{self.created_user.username}'s profile was successfully created."



