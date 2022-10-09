from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, MyPasswordChangeForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def change_password(request):
    form_class = MyPasswordChangeForm
    if request.method == 'POST':
        form = form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return render(request, 'password.html', {'form': form.as_p(), 'password_changed': True})
        else:
            return render(request, 'password.html', {'form': form.as_p(), 'password_changed': False})

    else:
        form = form_class(request.user)
        return render(request, 'password.html',{'form': form.as_p(),})
