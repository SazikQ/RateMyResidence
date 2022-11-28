from django import forms


class EmailVerificationForm(forms.Form):
    verificationCode = forms.CharField(max_length=10)


class ProfilePhotoForm(forms.Form):
    image = forms.ImageField()

