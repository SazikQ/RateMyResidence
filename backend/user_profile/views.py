import hashlib

from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from backend.user_authentication.forms import CustomUserChangeForm
from django.contrib import messages
from backend.user_profile.models import Review, ProfileImage, ResidenceRequest, RequestFile
from django.urls import reverse_lazy
import random
from backend.user_profile.forms import EmailVerificationForm, ProfilePhotoForm, RequestForm
from django.views.generic import TemplateView, ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist

@login_required
def profile(request):
    try:
        pic = ProfileImage.objects.get(belonged_user=request.user)
    except ObjectDoesNotExist:
        pic = None
    return render(request, 'account.html', {'profilePic': pic})


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
        verificationCode = ''
        for _ in range(6):
            verificationCode = verificationCode + str(random.randint(0,9))
        request.user.email_user('Email Verification', verificationCode, from_email=None)
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


@login_required
def profile_photo(request):
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                previousPhoto = ProfileImage.objects.get(belonged_user=request.user)
                previousPhoto.delete()
            except ObjectDoesNotExist:
                pass
            image = form.cleaned_data["image"]
            newPhoto = ProfileImage.objects.create(photo=image, belonged_user=request.user)
            newPhoto.save()
            messages.success(request, 'Your profile photo is updated successfully')
            return redirect(to='profile')
    else:
        form = ProfilePhotoForm

    return render(request, 'edit_profile_pic.html', {'photo_form': ProfilePhotoForm})

@login_required
def manager_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            selectedResidence = form.cleaned_data['selected_residence']
            try:
                previous_reqeust = ResidenceRequest.objects.get(requestResidence=selectedResidence, belonged_user=request.user)
                previous_reqeust.delete()
            except ObjectDoesNotExist:
                pass

            residence_request = ResidenceRequest.objects.create(requestResidence=selectedResidence, belonged_user=request.user)
            files = request.FILES.getlist('request_file')
            for file in files:
                RequestFile.objects.create(file=file, belonged_request=residence_request)
            return redirect(to='profile')
    else:
        form = RequestForm()

    return render(request, 'manager_request.html', {'form': form})
