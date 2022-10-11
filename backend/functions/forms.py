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
