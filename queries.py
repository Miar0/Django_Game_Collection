import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from games.models import Game, Review
from django.db.models import Count


print("--- 1. Усі записи головної моделі ---")
all_reviews = Review.objects.all()
print('1:', list(all_reviews))


print("\n--- 2. Фільтр за числовим полем (оцінка >= 8) ---")
high_rated = Review.objects.filter(rating__gte=8)
print('2:', list(high_rated))


print("\n--- 3. Фільтр за пов'язаною моделлю (ігри, доступні в Steam) ---")
steam_reviews = Review.objects.filter(game__platforms__name='Steam').distinct()
print('3:', list(steam_reviews))


print("\n--- 4. Фільтр за полем choices (статус 'Пройдено') ---")
completed_reviews = Review.objects.filter(status=Review.StatusChoices.COMPLETED)
print('4:', list(completed_reviews))


print("\n--- 5. Сортування + обмеження (топ-3 гри за оцінкою) ---")
top_3_reviews = Review.objects.order_by('-rating')[:3]
print('5:', list(top_3_reviews))


print("\n--- 6. Підрахунок через annotate (скільки платформ у кожної гри) ---")
games_with_platform_count = Game.objects.annotate(platform_count=Count('platforms'))
for i, game in enumerate(games_with_platform_count, start=1):
    print(f"{i}: Гра '{game.name}' доступна на {game.platform_count} платформах")


print("\n--- 7. Будь-який запит + вивід його SQL через .query ---")
complex_query = Review.objects.filter(
    rating__gt=7,
    game__platforms__name='Epic Games'
).distinct()

print('7 Result:', list(complex_query))
print('7 SQL Query:')
print(complex_query.query)