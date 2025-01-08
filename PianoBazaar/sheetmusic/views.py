import profile

import numpy as np
import pandas as pd
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count, Sum, F, Q, Value, OuterRef, Subquery
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from sklearn.metrics.pairwise import cosine_similarity

from sheetmusic.forms import ScoreCreateForm, CheckoutForm, ProfileUpdateForm
from sheetmusic.models import Score, Profile, BillingProfile


@csrf_exempt
@login_required
def toggle_like(request, score_pk):
    if request.method == 'POST':
        score = Score.objects.get(pk=score_pk)
        user_profile = request.user.profile

        if score in user_profile.liked_scores.all():
            user_profile.liked_scores.remove(score)
            liked = False
        else:
            user_profile.liked_scores.add(score)
            liked = True

        return JsonResponse({'liked': liked})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def toggle_score_in_shopping_cart(request, score_pk):
    if request.method == 'POST':
        score = Score.objects.get(pk=score_pk)
        profile = request.user.profile
        carted = profile.toggle_score_in_shopping_cart(score)
        return JsonResponse({'carted': carted})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def remove_score_from_shopping_cart(request, score_pk):
    score = Score.objects.get(pk=score_pk)
    profile = request.user.profile
    profile.remove_score_from_shopping_cart(score)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/sheetmusic/'))


class ScoreList(ListView):
    model = Score
    template_name = 'sheetmusic/home.html'

    def get(self, request, *args, **kwargs):
        if 'q' in self.request.GET:
            s_string = self.request.GET['q'] or None
            if s_string is not None:
                return redirect('sheetmusic:search_score', s_string=s_string)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'scores'
        if 'next' in self.request.GET:
            messages.warning(self.request, 'You need to login in order to like scores.')

        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            # recommendation system
            profiles = Profile.objects.all()
            scores = Score.objects.all()


            purchase_matrix = np.array([
                [1 if score in profile.purchased_scores.all() or score.arranger.pk == profile.pk else 0 for score in scores]
                for profile in profiles
            ])

            items_labels = [f"Item {score.pk}" for score in scores]
            user_labels = [f"User {profile.pk}" for profile in profiles]

            purchase_df = pd.DataFrame(purchase_matrix, index=user_labels, columns=items_labels)
            print(f"Matrice acquisti: \n"
                  f"{purchase_df}")

            profiles_similarity = cosine_similarity(purchase_matrix)
            similarity_df = pd.DataFrame(profiles_similarity, index=user_labels, columns=user_labels)

            print("\nMatrice di similarità tra utenti:")
            print(similarity_df.round(4))

            similarity_list = [(row + 1, col + 1, float(profiles_similarity[row, col]))
                               for row in range(profiles_similarity.shape[0])
                               for col in range(row + 1, profiles_similarity.shape[1])]

            print()
            for row, col, similarity in similarity_list:
                print(f"Similarità utente {row} e utente {col} = {round(similarity, 4)}")
            print()
            # print("\nLista delle similarità:", similarity_list)
            # print()

            rec_matrix = np.zeros_like(purchase_matrix, dtype=float)

            # calcolo tabella dei ranks
            for row in range(purchase_matrix.shape[0]):
                for col in range(purchase_matrix.shape[1]):

                    if purchase_matrix[row, col] != 1:  # se non ha acquistato questo item
                        mark = 0
                        for row2 in range(purchase_matrix.shape[0]):
                            mark += purchase_matrix[row2, col] * profiles_similarity[row2, row]
                        rec_matrix[row, col] = mark

            ranks_matrix = pd.DataFrame(rec_matrix, index=user_labels, columns=items_labels)
            print("Tabella con item ranks per ogni utente:")
            print(ranks_matrix.round(4))
            print()

            cur_user_pk = Profile.objects.get(user=self.request.user).pk

            cur_user_ranks = ranks_matrix.loc[f'User {str(cur_user_pk)}']
            sorted_ranks = cur_user_ranks.sort_values(ascending=False)
            top3 = sorted_ranks.head(3)

            score_keys = []
            for i in range (3):
                if top3.iloc[i] != 0: # if grade is not zero, so we are not recommending it just bcs we don't have anything to recommend
                    score_keys.append(top3.index[i].split(' ')[1])


            recommended_score_list = [Score.objects.get(pk=score_key) for score_key in score_keys]
            print("Recommended scores:")
            print(score_keys)
            print(recommended_score_list)
            print()

            context['recommended_score_list'] = recommended_score_list


        return context


class SearchScore(ListView):
    model = Score
    template_name = 'sheetmusic/score_search_results.html'

    def get_queryset(self):
        s_string = self.request.resolver_match.kwargs['s_string']
        # Restituisce un QuerySet contenente tutti gli oggetti che soddisfano almeno una delle condizioni specificate. I duplicati vengono scartati.
        result_scores = Score.objects.filter(
            Q(title__icontains=s_string) |
            Q(arranger__user__username__icontains=s_string) |
            Q(arranger__user__last_name__icontains=s_string)
        )
        return result_scores

class FilterScoreOnGenre(ListView):
    model = Score
    template_name = 'sheetmusic/score_search_results.html'

    def get_queryset(self):
        genre = self.request.resolver_match.kwargs['genre']
        # Restituisce un QuerySet contenente tutti gli oggetti che soddisfano almeno una delle condizioni specificate. I duplicati vengono scartati.
        result_scores = Score.objects.filter(
            Q(genre_1__icontains=genre) |
            Q(genre_2__icontains=genre)
        )
        return result_scores


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
        messages.success(request, 'The score has been deleted.')
        previous_url = request.META.get('HTTP_REFERER', '/sheetmusic/')
        return redirect(previous_url)

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

    def get(self, request, *args, **kwargs):
        if 'q' in self.request.GET:
            s_string = self.request.GET['q'] or None
            if s_string is not None:
                return redirect('sheetmusic:search_profile', s_string=s_string)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Profile.objects.annotate(
            score_count=Count('score', distinct=True),
            n_sold_copies=Count('score__sold_copies'),
            n_purchased_scores = Count('purchased_scores'),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'profiles'
        return context

class SearchProfile(ListView):
    model = Profile
    template_name = 'sheetmusic/profile_search_results.html'

    def get_queryset(self):
        s_string = self.request.resolver_match.kwargs['s_string']

        result_scores = Profile.objects.annotate(
            full_name = Concat('user__first_name', Value(' '), 'user__last_name')
        ).filter(
            Q(user__username__icontains=s_string) |
            Q(user__first_name__icontains=s_string) |
            Q(user__last_name__icontains=s_string) |
            Q(full_name__icontains=s_string)
        ).annotate(
            score_count=Count('score', distinct=True),
            likes_count=Count('score__liked_by'),)
        return result_scores


class ArrangerDetail(DetailView):
    model = Profile
    template_name = 'sheetmusic/arranger_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        scores = self.object.score.all()
        score_with_earnings = scores.annotate(
             n_sold_copies=Count('sold_copies'),
        )
        total_copies = score_with_earnings.aggregate(
            total=Sum('n_sold_copies')
        )['total'] or 0

        context['my_scores_list'] = Score.objects.filter(arranger=self.object)
        context['n_sold_copies'] = total_copies
        context['n_purchased_scores'] = self.object.purchased_scores.count()
        context['n_likes_received'] = scores.aggregate(
            total=Sum('liked_by')
        )['total'] or 0

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


class ArrangerViewShoppingCart(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'sheetmusic/profile_shopping_cart.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        total_price = 0
        for score in profile.shopping_cart.all():
            total_price += float(score.price)
        total_price = round(total_price, 2)
        context['total_price'] = total_price
        return context

@staff_member_required
def profile_delete(request, profile_pk):
    if request.method == 'POST':
        profile = Profile.objects.get(pk=profile_pk)
        user = User.objects.get(pk=profile.user_id)
        b_profile = BillingProfile.objects.get(user=user)

        b_profile.delete()
        profile.delete()
        user.delete()

        messages.success(request, 'The account has been deleted.')
        previous_url = request.META.get('HTTP_REFERER', '/sheetmusic/')
        return redirect(previous_url)

    previous_url = request.META.get('HTTP_REFERER', '/sheetmusic/')
    request.session['delete_profile_modal'] = 'show'
    request.session['delete_profile_name'] = Profile.objects.get(pk=profile_pk).user.username
    request.session['delete_profile_pk'] = profile_pk
    return redirect(previous_url)

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

    def form_valid(self, form):  # aggiungere azioni aggiuntive post form-validation prima della reindirizzazione.
        # invio pdf per email
        profile = Profile.objects.get(user=self.object.user)
        user_name = profile.user.username
        email = EmailMessage(
            subject="Your PianoBazaar Sheet Music Order",
            body=f"Dear {user_name},\n\n"
                 "Thank you for purchasing from PianoBazaar!\n\n"
                 "We’re delighted to share the sheet music you’ve ordered, attached as a PDF to this email.\n"
                 "We hope it brings joy and inspiration to your musical journey.\n\n"
                 # "If you have any questions, concerns, or need assistance with your order, please don’t hesitate to reach out to us at [support@pianobazaar.com].\n"
                 "Thank you for choosing PianoBazaar. We look forward to serving you again soon!\n\n"
                 "Warm regards,\n"
                 "The PianoBazaar Team",

            from_email='pianobazaar@example.com',
            to=[form.cleaned_data['receiving_email']],
        )


        for score in profile.shopping_cart.all():
            cleaned_url = 'media/' + score.file.url.lstrip('/media')
            print(cleaned_url)
            with open(cleaned_url, 'rb') as pdf_file:
                email.attach(f'{score.title}.pdf', pdf_file.read(), 'application/pdf')

        email.send()

        return super().form_valid(form)

    def get_success_url(self):
        profile = Profile.objects.get(user=self.request.user)
        for score in profile.shopping_cart.all():
            profile.add_purchased_score(score)
        profile.shopping_cart.clear()
        messages.success(self.request, f"Thanks {self.request.user.username}, the order was successful!")
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

        total_copies = score_with_earnings.aggregate(
            total=Sum('n_sold_copies')
        )['total'] or 0

        context['score_with_earnings'] = score_with_earnings
        context['total_earnings'] = round(total_earnings, 2)
        context['total_copies_sold'] = total_copies
        return context
