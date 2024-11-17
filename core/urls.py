from django.urls import path

import core.views

urlpatterns = [
    path("", core.views.home, name="home"),
    path("recipes/", core.views.RecipeListView.as_view(), name="recipe_list"),
    path("recipes/filter/", core.views.RecipeFilterView.as_view(), name="recipe_filter"),
    path("recipes/ingredient/<str:slug>", core.views.RecipeIngredientView.as_view(), name="recipe_ingredient"),
    path("recipes/my/", core.views.RecipeMyView.as_view(), name="recipe_my"),
    path("recipes/favorite/", core.views.RecipeFavoriteView.as_view(), name="recipe_favorite"),
    path("recipes/create/", core.views.RecipeCreateView.as_view(), name="recipe_create"),
    path("recipes/<int:pk>/", core.views.RecipeDetailView.as_view(), name="recipe_detail"),
    path("recipes/<int:pk>/add_comment", core.views.RecipeCommentAddView.as_view(), name="recipe_comment"),
    path("recipes/<int:pk>/update", core.views.RecipeUpdateView.as_view(), name="recipe_update"),
    path("recipes/<int:pk>/delete", core.views.RecipeDeleteView.as_view(), name="recipe_delete"),
    path("recipes/<int:pk>/add_to_favorite", core.views.RecipeAddToFavorites.as_view(), name="recipe_add_to_favorite"),
    path("recipes/<int:pk>/publish", core.views.recipe_publish, name="recipe_publish"),
    path("recipes/<int:pk>/add_ingredient", core.views.add_ingredient, name="add_ingredient"),
    path("recipes/delete_ingredient/<int:pk>", core.views.delete_ingredient, name="delete_ingredient"),
]
