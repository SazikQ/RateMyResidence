from email.policy import default
from pickle import FALSE
from django import forms
from taggit.forms import *
from backend.user_profile.models import Review


class ResidenceForm(forms.Form):
    name = forms.CharField(label='Residence name', max_length=100)
    streetName = forms.CharField(max_length=100)
    streetNum = forms.CharField(max_length=20)
    zipcode = forms.CharField(max_length=6)
    residence_tags = TagField()

class ResidenceEditForm(forms.Form):
    name = forms.CharField(label='Residence name', max_length=100)
    streetName = forms.CharField(max_length=100)
    streetNum = forms.CharField(max_length=20)
    zipcode = forms.CharField(max_length=6)

class ReviewForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(max_length=500)
    isAnonymous = forms.BooleanField(label = "Post Anonymously?", initial=False, required=False)

class EditReview(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(max_length=500)
    isAnonymous = forms.BooleanField(label = "Post Anonymously?", initial=False, required=False)

class DeleteReview(forms.Form):
    isDelete = forms.BooleanField(label="Delete post", initial=False, required=False)
    notDelete = forms.BooleanField(label = "Not delete post", initial=False, required=False)