from django.contrib import admin
from .models import Game, Platform, Review


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_platforms')
    search_fields = ('name',)
    filter_horizontal = ('platforms',)

    @admin.display(description='PLATFORMS')
    def get_platforms(self, obj):
        return ", ".join([platform.name for platform in obj.platforms.all()])

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('platforms')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('game', 'rating', 'status', 'comment', 'created_at')
    list_filter = ('status', 'rating')
    search_fields = ('game__name', 'comment')
    list_editable = ('status', 'rating')
