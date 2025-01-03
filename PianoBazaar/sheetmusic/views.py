import profile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, F
from django.db.models.functions import Round
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from PianoBazaar.forms import ProfileCreationForm
from sheetmusic.context_processor import user_profile_context
from sheetmusic.forms import ScoreCreateForm, CheckoutForm, ProfileUpdateForm
from sheetmusic.models import Score, Profile, BillingProfile, Copy


@login_required
def like_score(request, score_pk):
    score = Score.objects.get(pk=score_pk)
    profile = request.user.profile
    profile.toggle_like(score)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/sheetmusic/'))


@login_required
def manage_score_for_shopping_cart(request, score_pk):
    score = Score.objects.get(pk=score_pk)
    profile = request.user.profile
    profile.toggle_score_in_shopping_cart(score)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/sheetmusic/'))
    # si genera un errore quando l'utente cerca di metterlo nel carrello da non loggato perchè dopo aver fatto il login vieni reindirizzato
    # a questa pagina che però ti reinderizza alla pagina che chiama questa vista quindi ritorna nella pagina di login_required (la logica viene però eseguita correttamente)


class ScoreList(ListView):
    model = Score
    template_name = 'sheetmusic/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'scores'
        if 'next' in self.request.GET:
            messages.warning(self.request, 'You need to login in order to like scores.')
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

    def form_valid(self, form):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        form.instance.arranger = profile
        return super().form_valid(form)


@login_required
def score_delete(request, score_pk):
    if request.method == 'POST':
        Score.objects.get(pk=score_pk).delete()
        messages.success(request, 'Your score has been deleted.')
        return redirect('sheetmusic:arranger', Profile.objects.get(user=request.user).pk)

    previous_url = request.META.get('HTTP_REFERER', '/sheetmusic/')
    request.session['delete_score_modal'] = 'show'
    request.session['delete_score_name'] = Score.objects.get(pk=score_pk).title
    request.session['delete_score_pk'] = score_pk
    return redirect(previous_url)


class ScoreDetail(DetailView):
    model = Score
    template_name = 'sheetmusic/score_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ScoreVisualize(LoginRequiredMixin, DetailView):
    model = Score
    template_name = 'sheetmusic/score_visualize.html'
    context_object_name = 'score'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        score = Score.objects.get(pk=self.kwargs['pk'])
        context['pages'] = range(score.pages)
        return context

class ArrangerList(ListView):
    model = Profile
    template_name = 'sheetmusic/arranger_list.html'

    def get_queryset(self):
        return Profile.objects.annotate(
            score_count=Count('score', distinct=True),
            likes_count=Count('score__liked_by'),
        )

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
        try:
            context['delete_score_modal'] = self.request.session.pop('delete_score_modal', None)
            context['delete_score_name'] = self.request.session.pop('delete_score_name', None)
            context['delete_score_pk'] = self.request.session.pop('delete_score_pk', None)
        except: pass
        return context


class ArrangerDetailLikedScores(DetailView):
    model = Profile
    template_name = 'sheetmusic/arranger_detail_liked_scores.html'
    context_object_name = 'profile'


class ArrangerDetailPurchasedScores(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'sheetmusic/arranger_detail_purchased_scores.html'
    context_object_name = 'profile'

class ProfileUpdate(UpdateView):
    model = Profile
    template_name = 'sheetmusic/profile_update.html'
    form_class = ProfileUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('sheetmusic:arranger', kwargs={'pk': pk})

@login_required
def pre_checkout(request, score_pk):
    score = Score.objects.get(pk=score_pk)
    profile = request.user.profile
    profile.add_score_to_shopping_cart(score)
    b_profile = BillingProfile.objects.get(user=request.user)
    return redirect('sheetmusic:checkout', b_profile.pk)

class Checkout(LoginRequiredMixin, UpdateView):
    model = BillingProfile
    form_class = CheckoutForm
    template_name = 'sheetmusic/checkout.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user.pk)
        total_price = 0
        for score in profile.shopping_cart.all():
            total_price += float(score.price)
        total_price = round(total_price, 2)
        context['total_price'] = total_price
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        profile = Profile.objects.get(user=self.request.user)
        for score in profile.shopping_cart.all():
            profile.add_purchased_score(score)
        profile.shopping_cart.clear()
        return reverse_lazy('sheetmusic:arranger_purchased_scores', kwargs={'pk': profile.pk})


class SalesInsights(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'sheetmusic/sales_insights.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        scores = profile.score.all()

        score_with_earnings = scores.annotate(
            total_earnings=Sum(F('sold_copies__score__price')), n_sold_copies=Count('sold_copies'), #F permette di accedere a un campo del model
        )

        total_earnings = score_with_earnings.aggregate(
            total=Sum('total_earnings')
        )['total'] or 0

        context['score_with_earnings'] = score_with_earnings
        context['total_earnings'] = round(total_earnings, 2)
        return context
