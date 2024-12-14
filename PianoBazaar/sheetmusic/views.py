from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from sheetmusic.forms import CreateSheetForm
from sheetmusic.models import Score, Profile


def sheetmusic_home(request):
    return render(request, template_name='sheetmusic/home.html')

class ScoreList(ListView):
    model = Score
    template_name = 'sheetmusic/score_list.html'


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