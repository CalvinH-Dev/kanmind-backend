from django.urls import URLPattern, path

from .views import EmailCheckView, LoginView, RegistrationView

urlpatterns: list[URLPattern] = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path("email-check/", EmailCheckView.as_view(), name="email-check"),
]
