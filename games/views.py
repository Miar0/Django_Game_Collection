from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from .models import Game, Platform


def game_list(request):
    games = Game.objects.prefetch_related('platforms')
    return render(request, 'game_list.html', {'games': games})


def game_detail(request, pk):
    game = get_object_or_404(
        Game.objects.prefetch_related('platforms', 'reviews'),
        pk=pk
    )
    return render(request, 'game_detail.html', {'game': game})


def platform_list(request):
    platforms = Platform.objects.annotate(games_count=Count('games'))
    return render(request, 'platform_list.html', {'platforms': platforms})