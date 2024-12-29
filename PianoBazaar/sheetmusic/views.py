from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from sheetmusic.forms import ScoreCreateForm
from sheetmusic.models import Score, Profile


def like_score(request, score_pk):
    score = Score.objects.get(pk=score_pk)
    profile = request.user.profile
    profile.toggle_like(score)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/sheetmusic/'))


class ScoreList(ListView):
    model = Score
    template_name = 'sheetmusic/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'scores'
        try:
            context['arranger'] = Profile.objects.get(user=self.request.user)
        except:
            pass
        return context

class ScoreCreate(LoginRequiredMixin, CreateView):
    model = Score
    form_class = ScoreCreateForm
    template_name = 'sheetmusic/score_create.html'
    success_url = reverse_lazy("sheetmusic:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'upload score'
        return context

class ScoreDetail(DetailView):
    model = Score
    template_name = 'sheetmusic/score_detail.html'

class ArrangerList(ListView):
    model = Profile
    template_name = 'sheetmusic/arranger_list.html'

    def get_queryset(self):
        return Profile.objects.annotate(score_count=Count('score'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'profiles'
        return context

class ArrangerDetail(DetailView):
    model = Profile
    template_name = 'sheetmusic/arranger_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_scores_list'] = Score.objects.filter(arranger=self.object)
        return context

class ArrangerDetailLikedScores(DetailView):
    model = Profile
    template_name = 'sheetmusic/arranger_detail_liked_scores.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class ArrangerDetailPurchasedScores(DetailView):
    model = Profile
    template_name = 'sheetmusic/arranger_detail_purchased_scores.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

