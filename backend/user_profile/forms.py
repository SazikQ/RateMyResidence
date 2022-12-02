from django import forms
from backend.user_profile.models import Residence

class EmailVerificationForm(forms.Form):
    verificationCode = forms.CharField(max_length=10)


class ProfilePhotoForm(forms.Form):
    image = forms.ImageField()


class RequestForm(forms.Form):
    selected_residence = forms.ModelChoiceField(queryset=Residence.objects.all(), empty_label=None, 
                        widget=forms.Select(attrs={'class':'form-select'}))
