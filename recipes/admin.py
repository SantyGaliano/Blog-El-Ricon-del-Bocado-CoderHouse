from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'created_at')
    search_fields = ('name', 'difficulty')
    list_filter = ('difficulty',)
