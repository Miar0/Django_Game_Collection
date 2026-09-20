from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Game, Platform, Review


# def game_list(request):
#     games = Game.objects.prefetch_related('platforms')
#     return render(request, 'game_list.html', {'games': games})
#
# def game_detail(request, pk):
#     game = get_object_or_404(
#         Game.objects.prefetch_related('platforms', 'reviews'),
#         pk=pk
#     )
#     return render(request, 'game_detail.html', {'game': game})
#
# def platform_list(request):
#     platforms = Platform.objects.annotate(games_count=Count('games'))
#     return render(request, 'platform_list.html', {'platforms': platforms})


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class OwnerOrStaffRequiredMixin(StaffRequiredMixin):
    def test_func(self):
        if super().test_func():
            return True
        obj = self.get_object()
        return obj.owner == self.request.user


class GameListView(ListView):
    queryset = Game.objects.prefetch_related('platforms')
    template_name = 'games/game_list.html'
    context_object_name = 'games'
    ordering = ['name']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_platforms'] = Platform.objects.all()
        return context


class FilteredGameListView(ListView):
    model = Game
    template_name = 'games/game_list.html'
    context_object_name = 'games'
    paginate_by = 5

    def get_queryset(self):
        qs = Game.objects.prefetch_related('platforms')

        platform_id = self.request.GET.get('platform')
        if platform_id:
            qs = qs.filter(platforms__id=platform_id)

        search_query = self.request.GET.get('q')
        if search_query:
            qs = qs.filter(name__icontains=search_query)

        min_rating = self.request.GET.get('min_rating')
        if min_rating:
            qs = qs.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=min_rating)

        return qs.distinct().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_platforms'] = Platform.objects.all()
        return context


class GameDetailView(DetailView):
    queryset = Game.objects.prefetch_related('platforms', 'reviews')
    template_name = 'games/game_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_platforms = self.object.platforms.all()
        context['related_games'] = (
            Game.objects.filter(platforms__in=current_platforms)
            .exclude(pk=self.object.pk)
            .distinct()[:5]
        )
        return context


class GameCreateView(StaffRequiredMixin, CreateView):
    model = Game
    fields = ['name', 'platforms']
    template_name = 'games/game_form.html'


class GameUpdateView(StaffRequiredMixin, UpdateView):
    model = Game
    fields = ['name', 'platforms']
    template_name = 'games/game_form.html'


class GameDeleteView(StaffRequiredMixin, DeleteView):
    model = Game
    template_name = 'games/game_confirm_delete.html'
    success_url = reverse_lazy('game_list')


class PlatformListView(ListView):
    queryset = Platform.objects.annotate(games_count=Count('games')).order_by('name')
    template_name = 'games/platform_list.html'
    context_object_name = 'platforms'


class PlatformCreateView(StaffRequiredMixin, CreateView):
    model = Platform
    fields = ['name']
    template_name = 'games/platform_form.html'
    success_url = reverse_lazy('platform_list')


class PlatformUpdateView(StaffRequiredMixin, UpdateView):
    model = Platform
    fields = ['name']
    template_name = 'games/platform_form.html'
    success_url = reverse_lazy('platform_list')


class PlatformDeleteView(StaffRequiredMixin, DeleteView):
    model = Platform
    template_name = 'games/platform_confirm_delete.html'
    success_url = reverse_lazy('platform_list')


class MyReviewsView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'games/my_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        qs = (
            Review.objects.filter(owner=self.request.user)
            .select_related('game')
            .order_by('-created_at')
        )

        search_query = self.request.GET.get('q')
        if search_query:
            qs = qs.filter(game__name__icontains=search_query)

        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)

        min_rating = self.request.GET.get('min_rating')
        if min_rating:
            qs = qs.filter(rating__gte=min_rating)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Review.StatusChoices.choices
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'status', 'comment']
    template_name = 'games/review_form.html'

    def form_valid(self, form):
        game = get_object_or_404(Game, pk=self.kwargs['game_pk'])
        form.instance.game = game
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = get_object_or_404(Game, pk=self.kwargs['game_pk'])
        return context


class ReviewUpdateView(OwnerOrStaffRequiredMixin, UpdateView):
    model = Review
    fields = ['rating', 'status', 'comment']
    template_name = 'games/review_form.html'



class ReviewDeleteView(OwnerOrStaffRequiredMixin, DeleteView):
    model = Review
    template_name = 'games/review_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('game_detail', kwargs={'pk': self.object.game.pk})
