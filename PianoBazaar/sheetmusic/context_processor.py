from .models import Profile

def user_profile_context(request):
    context = {}

    if request.user.is_authenticated:
        try:
            context['user_profile'] = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            context['user_profile'] = None

    context['logout_modal'] = request.session.pop('logout_modal', None)

    return context
