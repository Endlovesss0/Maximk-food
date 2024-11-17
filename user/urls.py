from django.contrib.auth.views import LogoutView
from django.urls import path

from user.views import UserLoginView, UserRegisterView, UserDetailView, UserUpdateInfoView, UserUpdateMainInfoView, \
    UserUpdateAdditionalInfoView, ContactView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("info/<slug:username>/", UserDetailView.as_view(), name="user_info"),
    path("info/<slug:username>/update_info/", UserUpdateInfoView.as_view(), name="user_update_info"),
    path("info/<slug:username>/update_main_info/", UserUpdateMainInfoView.as_view(), name="user_update_main_info"),
    path("info/<slug:username>/update_additional_info/", UserUpdateAdditionalInfoView.as_view(),
         name="user_update_additional_info"),
    path("contact_us/", ContactView.as_view(), name="user_contact_us"),
]
