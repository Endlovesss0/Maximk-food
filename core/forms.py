import django.forms as forms

from core.models import Recipe, Comment


class RecipeCreationForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("title", "description")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"})
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("title", "description", "content", "image", "is_published")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text", "parent")
        widgets = {
            "parent": forms.HiddenInput()
        }
