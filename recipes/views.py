from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Recipe
from .forms import RecipeForm


class HomeView(TemplateView):
    template_name = 'recipes/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        ctx['recipes']   = Recipe.objects.order_by('-created_at')[:4]
       
        ctx['novedades'] = Recipe.objects.order_by('-created_at')[:8]
        return ctx


class RecipeListView(ListView):
    model               = Recipe
    template_name       = 'recipes/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        qs = Recipe.objects.order_by('-created_at')
        q  = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(difficulty__icontains=q) |
                Q(instructions__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx      = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class RecipeDetailView(DetailView):
    model               = Recipe
    template_name       = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model         = Recipe
    form_class    = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_url   = reverse_lazy('recipe-list')


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model         = Recipe
    form_class    = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_url   = reverse_lazy('recipe-list')


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model         = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url   = reverse_lazy('recipe-list')
