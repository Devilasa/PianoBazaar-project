from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from .models import Score, Profile


@receiver(post_save, sender=Score)
def generate_cover_on_save(sender, instance, created, **kwargs):

    if created and instance.file:
        instance.set_pages_number()
        instance.set_pdf_first_page_as_cover()


@receiver(user_logged_in)
def add_login_message(sender, request, user, **kwargs):
    if request is not None and user.is_authenticated:
        messages.success(request, f"Hi {user.username}, you successfully logged in!")

@receiver(user_logged_out)
def add_logout_message(sender, request, user, **kwargs):
    if request is not None and user.is_authenticated:
        messages.success(request,f"Bye {user.username}, hope to see you soon!")
