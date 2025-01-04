from .models import Profile

def user_profile_context(request):
    context = {}

    if request.user.is_authenticated:
        try:
            context['user_profile'] = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            context['user_profile'] = None

    context['logout_modal'] = request.session.pop('logout_modal', None)

    if request.user.is_superuser or request.user.is_staff:
        context['delete_score_modal'] = request.session.pop('delete_score_modal', None)
        context['delete_score_name'] = request.session.pop('delete_score_name', None)
        context['delete_score_pk'] = request.session.pop('delete_score_pk', None)

        context['delete_profile_modal'] = request.session.pop('delete_profile_modal', None)
        context['delete_profile_name'] = request.session.pop('delete_profile_name', None)
        context['delete_profile_pk'] = request.session.pop('delete_profile_pk', None)

    return context
