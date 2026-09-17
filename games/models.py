from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Platform(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('platform_list')

class Game(models.Model):
    name = models.CharField(max_length=100)
    platforms = models.ManyToManyField(Platform, related_name='games')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})


class Review(models.Model):
    class StatusChoices(models.TextChoices):
        PLANNED = 'planned', 'В планах'
        PLAYING = 'playing', 'Граю'
        COMPLETED = 'completed', 'Пройдено'
        ABANDONED = 'abandoned', 'Покинуто'

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PLANNED,
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.game.name} ({self.get_status_display()}) - {self.rating}/10"

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.game.pk})