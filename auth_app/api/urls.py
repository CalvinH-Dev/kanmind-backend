from django.urls import URLPattern, path

from .views import RegistrationView

urlpatterns: list[URLPattern] = [
    path("registration/", RegistrationView.as_view(), name="registration"),
]
