from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from backend.user_authentication.forms import CustomUserChangeForm


def profile(request):
    return render(request, 'account.html')


class EditProfileView(CreateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('profile')
    template_name = "editprofile.html"
