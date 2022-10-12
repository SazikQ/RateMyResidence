from email.policy import default
from pickle import FALSE
from django import forms
from taggit.forms import *


class ResidenceForm(forms.Form):
    name = forms.CharField(label='Residence name', max_length=100)
    streetName = forms.CharField(max_length=100)
    streetNum = forms.CharField(max_length=20)
    zipcode = forms.CharField(max_length=6)
    residence_tags = TagField()


class ReviewForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(max_length=500)
    isAnonymous = forms.BooleanField(label = "Post Anonymously?", initial=False, required=False)
    rating = forms.DecimalField(min_value=0, max_value=5)
    # class Meta:
    #     model = Review
    #     fields = ('title', 'content')

    #     widgets = {
    #         'title': forms.TextInput(),
    #         'content': forms.Textarea(),
    #     }