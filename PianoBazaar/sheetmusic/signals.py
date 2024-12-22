from django.contrib.auth.signals import user_logged_in
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
    request.session['welcome_message'] = f"Hi {user.username}, you have successfully logged in!"


