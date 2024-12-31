from .models import Profile

def user_profile_context(request):
    if request.user.is_authenticated:
        try:
            return {'user_profile': Profile.objects.get(user=request.user)}
        except Profile.DoesNotExist:
            return {'user_profile': None}
    return {}