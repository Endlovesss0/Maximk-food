from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


class Ingredient(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=False, verbose_name="Назва")
    slug = models.SlugField(unique=True, verbose_name="Slug")

    def get_absolute_url(self):
        return reverse("recipe_ingredient", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Інгредієнт"
        verbose_name_plural = "Інгредієнт"


class Recipe(models.Model):
    title = models.CharField(max_length=150, blank=False, verbose_name="Назва")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    content = RichTextUploadingField(blank=True, null=True, verbose_name="Рецепт")
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient", related_name="recipes",
                                         verbose_name="Інгредієнти")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes", verbose_name="Користувач")
    image = models.ImageField(upload_to="recipe_images", verbose_name="Фото", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створений")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлений")
    is_published = models.BooleanField(default=False, verbose_name="Опубліковано")
    favorited_by = models.ManyToManyField(User, related_name="favorite_recipes", verbose_name="Обраний користувачами")
    views = models.PositiveIntegerField(default=1, verbose_name="Кількість переглядів")

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепти"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Інгредієнт")
    quantity = models.IntegerField(verbose_name="Кількість")
    unit = models.CharField(max_length=10, verbose_name="Одиниця виміру")

    def __str__(self):
        return self.recipe.title + " " + self.ingredient.name

    class Meta:
        verbose_name = "Інгредієнт рецепту"
        verbose_name_plural = "Інгредієнт рецептів"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name="comments")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт", related_name="comments")
    text = RichTextField(verbose_name="Текст коментара")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name="Батьківський коментар", null=True,
                               blank=True, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створений")

    def __str__(self):
        return f"{self.recipe.title} ({self.user.username} {self.created_at})"

    class Meta:
        verbose_name = "Коментар рецепту"
        verbose_name_plural = "Коментарі рецептів"
