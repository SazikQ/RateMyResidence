from django.urls import path
from django.views.generic import TemplateView
from .views import SignUpView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),

]