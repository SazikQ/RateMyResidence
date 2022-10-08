from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from backend.user_authentication.forms import CustomUserChangeForm
from django.contrib import messages



def profile(request):
    return render(request, 'account.html')


# class EditProfileView(CreateView):
#     form_class = CustomUserChangeForm
#     success_url = reverse_lazy('profile')
#     template_name = "editprofile.html"




@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = CustomUserChangeForm(instance=request.user)

    return render(request, 'editprofile.html', {'edit_form': user_form})
