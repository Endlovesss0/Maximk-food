from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, FormView

from user.forms import LoginForm, UserMainInfoForm, UserAdditionalInfoForm, ContactForm
from user.models import UserAdditionalInfo


class UserLoginView(LoginView):
    """Вход на сайт"""
    template_name = "user/login.html"
    authentication_form = LoginForm


class UserRegisterView(View):
    """Регистрация на сайте"""
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, "user/register.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect("home")
        else:
            return render(request, "user/register.html", context={"form": form})


class UserDetailView(DetailView):
    """Информация о пользователе"""
    slug_url_kwarg = "username"
    slug_field = "username"
    model = User
    context_object_name = "user"
    template_name = "user/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["additional_info"] = self.object.additional_info
        except ObjectDoesNotExist:
            context["additional_info"] = None
        return context


class SameUserMixin(UserPassesTestMixin):

    def test_func(self):
        """Проверяет, что пользователь тот же, что и редактируемый пользователь"""
        user = get_object_or_404(User, username=self.kwargs["username"])
        return self.request.user == user


class UserUpdateInfoView(LoginRequiredMixin, SameUserMixin, UserDetailView):
    """Страница для перехода на формы редактирования информации"""
    template_name = "user/update_info.html"


class UserUpdateMainInfoView(LoginRequiredMixin, SameUserMixin, UpdateView):
    """Страница для редактирования основной информации о пользователе"""
    model = User
    form_class = UserMainInfoForm
    slug_url_kwarg = "username"
    slug_field = "username"
    template_name = "user/update_main_info.html"
    context_object_name = "user"

    def form_valid(self, form):
        messages.success(self.request, "Данные успешно изменены!")
        self.success_url = reverse_lazy("user_update_info", kwargs=self.kwargs)
        return super().form_valid(form)


class UserUpdateAdditionalInfoView(LoginRequiredMixin, SameUserMixin, UpdateView):
    """Страница для редактирования дополнительной информации о пользователе"""
    model = UserAdditionalInfo
    form_class = UserAdditionalInfoForm
    slug_url_kwarg = "username"
    slug_field = "username"
    template_name = "user/update_additional_info.html"
    context_object_name = "info"

    def get_object(self, queryset=None):
        user = get_object_or_404(User, username=self.kwargs["username"])
        try:
            additional_info = user.additional_info
        except ObjectDoesNotExist:
            additional_info = UserAdditionalInfo.objects.create(user=user)
        return user.additional_info

    def form_valid(self, form):
        messages.success(self.request, "Данные успешно изменены!")
        self.success_url = reverse_lazy("user_update_info", kwargs=self.kwargs)
        return super().form_valid(form)


class ContactView(FormView):
    form_class = ContactForm
    template_name = "user/contact_us.html"
    success_url = reverse_lazy("user_contact_us")

    def form_valid(self, form):
        form.send_email_message()
        messages.success(self.request, "Ваше сообщение успешно отправлено!")
        return super().form_valid(form)
