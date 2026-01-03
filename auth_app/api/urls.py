from django.urls import URLPattern, path

from .views import LoginView, RegistrationView

urlpatterns: list[URLPattern] = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
]
