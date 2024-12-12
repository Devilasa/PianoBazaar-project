from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from sheetmusic.forms import CreateSheetForm
from sheetmusic.models import Score


def sheetmusic_home(request):
    return render(request, template_name='sheetmusic/home.html')

class SheetMusicList(ListView):
    model = Score
    template_name = 'sheetmusic/sheet_list.html'


class CreateSheetMusic(CreateView):
    model = Score
    form_class = CreateSheetForm
    template_name = 'sheetmusic/create_sheet.html'
    success_url = reverse_lazy("sheetmusic:sheet_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Load sheetmusic'
        context['message'] = 'Load new sheetmusic'
        return context
