from django.contrib.auth.forms import AuthenticationForm, UsernameField
import django.forms as forms
from django.contrib.auth.models import User
from django.core.mail import send_mail

from Recipes import settings
from user.models import UserAdditionalInfo


class LoginForm(AuthenticationForm):
    """Форма входа"""
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"}))
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control"}),
    )


class UserMainInfoForm(forms.ModelForm):
    """Форма редактирования основной информации"""
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class UserAdditionalInfoForm(forms.ModelForm):
    """Форма редактирования дополнительной информации"""
    class Meta:
        model = UserAdditionalInfo
        fields = ("avatar", "about", "date_of_birth", "place")
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "about": forms.Textarea(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(attrs={"class": "form-control"}),
            "place": forms.TextInput(attrs={"class": "form-control"}),
        }


class ContactForm(forms.Form):
    """Контактная форма"""
    name = forms.CharField(label="Ваше имя", max_length=100, min_length=1, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    message = forms.CharField(label="Сообщение", widget=forms.Textarea(attrs={"class": "form-control"}))

    def send_email_message(self):
        subject = f"Обратная связь DjangoRecipes от {self.cleaned_data['name']}"
        message = self.cleaned_data["message"] + f"\nEmail: {self.cleaned_data['email']}"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
