from django.http import HttpResponseForbidden

from sheetmusic.models import Profile, BillingProfile


class LicenseRequiredMixin:
    owner_field = 'arranger'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        score = self.get_object()
        owner = getattr(score, self.owner_field, None)
        cur_user_profile = Profile.objects.get(user=request.user)

        if owner != cur_user_profile and score not in cur_user_profile.purchased_scores.all():
            return HttpResponseForbidden("You don't have the license to visualize this score.")

        return super().dispatch(request, *args, **kwargs)

class OwnerRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        profile = self.get_object()
        cur_user_profile = Profile.objects.get(user=request.user)

        if profile.pk != cur_user_profile.pk:
            return HttpResponseForbidden("You don't have the right to complete this action.")

        return super().dispatch(request, *args, **kwargs)

class BillingProfileOwnerRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        billing_profile = self.get_object()
        cur_user_billing_profile = BillingProfile.objects.get(user=request.user)

        if billing_profile.pk != cur_user_billing_profile.pk:
            return HttpResponseForbidden("Don't try to fool us.")

        return super().dispatch(request, *args, **kwargs)

