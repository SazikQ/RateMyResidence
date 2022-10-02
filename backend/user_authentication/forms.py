from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from backend.user_profile.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "isVerifiedUser", "isResidenceManager")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username", "email", "isVerifiedUser", "isResidenceManager")

