from django import template

from core.models import Recipe

register = template.Library()


@register.inclusion_tag("user/templatetags/user_recipes.html")
def last_recipes(user, max_num):
    """Выводит последние рецепты пользователя в количестве до max_num"""
    recipes = Recipe.objects.filter(user=user, is_published=True).order_by("-created_at").defer("description",
                                                                                                "content")[0:3]
    return {"recipes": recipes}
