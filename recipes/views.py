from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q

from .models import Recipe
from .forms import RecipeForm


class Recipes(ListView):
    """
    Recipes List view
    """

    template_name = "recipes/recipes.html"
    model = Recipe
    context_object_name = "recipes"

    def get_queryset(self, **kwargs):
        query = self.request.GET.get("q")
        recipes = self.model.objects.all()

        if query:
            recipes = self.model.objects.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(instructions__icontains=query)
                | Q(cuisine_types__icontains=query)
            )
        elif "q" in self.request.GET:
            messages.error(self.request, "You didn't enter any search criteria")

        return recipes


class RecipeDetail(DetailView):
    """
    View a single recipe
    """

    template_name = "recipes/recipe_detail.html"
    model = Recipe
    context_object_name = "recipe"


class AddRecipe(LoginRequiredMixin, CreateView):
    """
    Add Recipe view
    """

    template_name = "recipes/add_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddRecipe, self).form_valid(form)


class EditRecipe(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit A Recipe
    """

    template_name = "recipes/edit_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def test_func(self):
        return self.request.user == self.get_object().user


class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a Recipe
    """

    model = Recipe
    success_url = "/recipes/"

    def test_func(self):
        return self.request.user == self.get_object().user
