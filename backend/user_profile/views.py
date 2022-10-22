import hashlib

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from backend.user_authentication.forms import CustomUserChangeForm
from django.contrib import messages
from backend.user_profile.models import Review
from django.urls import reverse_lazy
import random
from backend.user_profile.forms import EmailVerificationForm
from django.views.generic import TemplateView, ListView, DetailView


def profile(request):
    return render(request, 'account.html')


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


@login_required
def account_verify(request):
    if request.method == 'POST':
        verificationForm = EmailVerificationForm(request.POST)
        if verificationForm.is_valid():
            verificationCode = verificationForm.cleaned_data['verificationCode']
            actualHashcode = hashlib.sha256(verificationCode.encode('utf-8')).hexdigest()
            correctHashcode = request.session['hashcode']
            if actualHashcode == correctHashcode:
                request.user.isVerifiedUser = True
                request.user.save()
                messages.success(request, 'You account is now verified')
                return redirect(to='profile')
            else:
                messages.error(request, 'wrong verification code')
                return redirect(to='profile')
    else:
        verificationCode = '123456'
        '''
        for _ in range(6) :
            verificationCode = verificationCode + str(random.randint(0,9))
        request.user.email_user('Email Verification', verificationCode, from_email=None)
        '''
        verificationForm = EmailVerificationForm()
        hashcode = hashlib.sha256(verificationCode.encode('utf-8')).hexdigest()
        request.session['hashcode'] = hashcode

    return render(request, 'user_verify.html', {'form': verificationForm.as_p()})


@method_decorator(login_required, name='dispatch')
class ReviewHistoryView(ListView):
    model = Review
    paginate_by = 20
    template_name = 'review_list.html'

    def get_queryset(self):
        object_list = Review.objects.filter(reviewer=self.request.user)
        return object_list


class ReviewDetail(DetailView):
    model = Review
    template_name = 'review_info.html'
