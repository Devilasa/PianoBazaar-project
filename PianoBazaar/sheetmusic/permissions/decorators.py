from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from sheetmusic.models import Score, Profile


def user_is_owner(view_func):
    """
    Decoratore per garantire che l'utente autenticato sia il proprietario di un oggetto.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)

        object_id = kwargs.get('score_pk', None)
        if object_id is None:
            return HttpResponseForbidden("Object ID not provided.")

        try:
            score = Score.objects.get(pk=object_id)
        except Score.DoesNotExist:
            return HttpResponseForbidden("Object does not exist.")

        # Controlla se l'utente autenticato è il proprietario
        if score.arranger.user != request.user:
            return HttpResponseForbidden("You can't delete someone else's score.")

        # Passa il controllo alla vista
        return view_func(request, *args, **kwargs)

    return _wrapped_view

def deleted_profile_is_not_staff(view_func):
    """
    Decoratore per garantire che l'utente autenticato sia il proprietario di un oggetto.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        profile_id = kwargs.get('profile_pk', None)
        if profile_id is None:
            return HttpResponseForbidden("Object ID not provided.")

        try:
            profile = Profile.objects.get(pk=profile_id)
        except Profile.DoesNotExist:
            return HttpResponseForbidden("Object does not exist.")

        if profile.user.is_staff:
            return HttpResponseForbidden("Warning: you can't delete admins profiles!")

        return view_func(request, *args, **kwargs)

    return _wrapped_view