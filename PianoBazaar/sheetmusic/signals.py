from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Score


@receiver(post_save, sender=Score)
def generate_cover_on_save(sender, instance, created, **kwargs):

    if created and instance.file:

        instance.set_pages_number()
        instance.set_pdf_first_page_as_cover()


