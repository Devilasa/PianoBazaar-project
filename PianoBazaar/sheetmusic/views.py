from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from sheetmusic.forms import CreateSheetForm
from sheetmusic.models import Score, Profile


def sheetmusic_home(request):
    return render(request, template_name='sheetmusic/home.html')

class ScoreList(ListView):
    model = Score
    template_name = 'sheetmusic/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['welcome_message'] = self.request.session.pop('welcome_message', None)
        return context

class CreateSheetMusic(CreateView):
    model = Score
    form_class = CreateSheetForm
    template_name = 'sheetmusic/create_sheet.html'
    success_url = reverse_lazy("sheetmusic:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Load new sheetmusic'
        return context

class ScoreDetail(DetailView):
    model = Score
    template_name = 'sheetmusic/score_detail.html'

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
        # context['my_scores_list'] = Score.objects.filter(arranger=self.object)

        return context

class ArrangerDetailPurchasedScores(DetailView):
    model = Profile
    template_name = 'sheetmusic/arranger_detail_purchased_scores.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['my_scores_list'] = Score.objects.filter(arranger=self.object)

        return context

