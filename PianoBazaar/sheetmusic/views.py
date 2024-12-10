from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

def sheetmusic_home(request):
    return render(request, template_name='sheetmusic/home.html')


class CreateSheetMusic(CreateView):
    title = "add a score to the collection"
    template_name = 'sheetmusic/create_entry.html'
    fields = '__all__'
    success_url = reverse_lazy("sheetmusic:home")
