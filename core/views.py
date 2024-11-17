from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.db import DatabaseError
from django.views import View

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from core.forms import RecipeCreationForm, RecipeForm, CommentForm
from core.models import Recipe, RecipeIngredient, Ingredient, Comment


def _add_ingredients_to_context(context, recipe):
    ingredients = RecipeIngredient.objects.filter(recipe=recipe).select_related("ingredient")
    context["ingredients"] = ingredients
    return context


def home(request):
    return render(request, "home.html")


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = "recipe"

    def get_object(self, *args, **kwargs):
        recipe = super().get_object(*args, **kwargs)
        recipe.views += 1
        recipe.save(update_fields=["views"])

        recipe.is_favorite = recipe.favorited_by.filter(pk=self.request.user.pk).exists()

        return recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = _add_ingredients_to_context(context, self.object)

        comments = Comment.objects.filter(recipe=self.object).select_related("user__additional_info", "parent__user")\
            .order_by("-created_at")
        context["comments"] = comments

        context["comment_form"] = CommentForm()

        return context


class RecipeCommentAddView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["pk"])
        user = self.request.user

        comment_form = CommentForm(self.request.POST)
        if comment_form.is_valid():
            parent = comment_form.cleaned_data["parent"]
            if parent:
                parent = Comment.objects.get(pk=parent.pk)
                if parent.recipe != recipe:
                    messages.error(self.request, "Неможливо додати коментар!")
                    return redirect("recipe_detail", self.kwargs["pk"])

            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.user = user
            comment.save()
            messages.success(self.request, "Коментар доданий успішно!")
        else:
            messages.error(self.request, "Неможливо додати коментар!")

        return redirect("recipe_detail", self.kwargs["pk"])


class RecipeListView(ListView):
    model = Recipe
    queryset = Recipe.objects.filter(is_published=True)
    context_object_name = "recipes"
    paginate_by = 6


class RecipeFilterView(ListView):
    model = Recipe
    context_object_name = "recipes"
    template_name_suffix = "_filter"
    paginate_by = 6

    def get_queryset(self):
        queryset = Recipe.objects.filter(is_published=True)

        if "user" in self.request.GET:
            queryset = queryset.filter(user__username=self.request.GET.get("user"))
        if "title" in self.request.GET:
            queryset = queryset.filter(title__icontains=self.request.GET.get("title"))
        if "order_by" in self.request.GET:
            order_by = self.request.GET["order_by"]
            orderings = {
                "views": "-views",
                "title": "title",
                "oldest": "created_at",
                "newest": "-created_at",
            }
            if order_by in orderings:
                queryset = queryset.order_by(orderings[order_by])

        return queryset


class RecipeIngredientView(ListView):
    model = Recipe
    context_object_name = "recipes"
    template_name_suffix = "_ingredient"
    paginate_by = 6

    def get_queryset(self):
        ingredient = get_object_or_404(Ingredient, slug=self.kwargs.get("slug"))
        return ingredient.recipes.all()


class RecipeMyView(LoginRequiredMixin, ListView):
    model = Recipe
    context_object_name = "recipes"
    template_name_suffix = "_my"
    paginate_by = 6

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)


class RecipeFavoriteView(LoginRequiredMixin, ListView):
    model = Recipe
    context_object_name = "recipes"
    template_name_suffix = "_favorite"
    paginate_by = 6

    def get_queryset(self):
        return self.request.user.favorite_recipes.all()


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name_suffix = "_create"
    form_class = RecipeCreationForm

    def form_valid(self, form):
        messages.success(self.request,
                         "Рецепт успішно доданий, але ще не опубліковано. Змініть рецепт та опублікуйте його")
        form.instance.user = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    template_name_suffix = "_update"
    form_class = RecipeForm
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return _add_ingredients_to_context(context, self.object)

    def form_valid(self, form):
        messages.success(self.request, "Рецепт успішно змінено!")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().user


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    context_object_name = "recipe"
    success_url = reverse_lazy("recipe_list")

    def form_valid(self, form):
        messages.success(self.request, "Рецепт успішно вилучено!")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().user


class RecipeAddToFavorites(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["pk"])
        user = self.request.user

        if user.favorite_recipes.filter(pk=recipe.pk).exists():
            user.favorite_recipes.remove(recipe)
        else:
            user.favorite_recipes.add(recipe)

        return redirect("recipe_detail", self.kwargs["pk"])


@login_required
def recipe_publish(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.user:
        return HttpResponseForbidden()

    recipe.is_published = True
    recipe.save()
    messages.success(request, "Рецепт успішно опубліковано")
    return redirect("recipe_detail", pk=pk)


@login_required
def add_ingredient(request, pk):
    if request.method != "POST":
        return HttpResponseBadRequest

    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.user:
        return HttpResponseForbidden()

    name = request.POST["name"]
    quantity = request.POST["quantity"]
    unit = request.POST["unit"]

    try:
        ingredient = Ingredient.objects.filter(name=name)
        if ingredient.exists():
            ingredient = ingredient[0]
        else:
            slug = slugify(name, allow_unicode=True)
            ingredient = Ingredient.objects.create(name=name, slug=slug)
        recipe_ingredient = RecipeIngredient(ingredient=ingredient, recipe=recipe, quantity=quantity, unit=unit)
        recipe_ingredient.save()
    except DatabaseError:
        messages.error(request, "Неможливо додати інгредієнт!")

    return redirect("recipe_update", pk=recipe.pk)


@login_required
def delete_ingredient(request, pk):
    ingredient = get_object_or_404(RecipeIngredient, pk=pk)
    recipe = ingredient.recipe
    if request.user != recipe.user:
        return HttpResponseForbidden()

    ingredient.delete()

    return redirect("recipe_update", pk=recipe.pk)
