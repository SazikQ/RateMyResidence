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
    distance = forms.FloatField(min_value=0)
    residence_tags = TagField()

class ResidenceEditForm(forms.Form):
    name = forms.CharField(label='Residence name', max_length=100)
    streetName = forms.CharField(max_length=100)
    streetNum = forms.CharField(max_length=20)
    zipcode = forms.CharField(max_length=6)
    distance = forms.FloatField(min_value=0)
    website = forms.CharField(max_length=150)
    residence_tags = TagField()

class ReviewForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(max_length=500)
    isAnonymous = forms.BooleanField(label = "Post Anonymously?", initial=False, required=False)
    rating = forms.DecimalField(min_value=0, max_value=5)
    time_lived = forms.IntegerField(label= "How long have you been living in this residence (semester)?", required=False)
    live_again = forms.BooleanField(label= "Would you live in this residence again?", initial=False, required=False)
    rent = forms.IntegerField(label="How much are you paying for your residence a month?", required=False)
    location_rating = forms.DecimalField(min_value=0, max_value=5)
    quietness_rating = forms.DecimalField(min_value=0, max_value=5)
    quality_rating = forms.DecimalField(min_value=0, max_value=5)
    room_type = forms.ChoiceField(label="Select your room type", choices=Review.RoomType.choices)



class EditReview(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(max_length=500)
    isAnonymous = forms.BooleanField(label = "Post Anonymously?", initial=False, required=False)
    rating = forms.DecimalField(min_value=0, max_value=5)
    time_lived = forms.IntegerField(label= "How long have you been living in this residence (semester)?", required=False)
    live_again = forms.BooleanField(label= "Would you live in this residence again?", initial=False, required=False)
    rent = forms.IntegerField(label="How much are you paying for your residence a month?", required=False)
    location_rating = forms.DecimalField(min_value=0, max_value=5)
    quietness_rating = forms.DecimalField(min_value=0, max_value=5)
    quality_rating = forms.DecimalField(min_value=0, max_value=5)
    room_type = forms.ChoiceField(label="Select your room type", choices=Review.RoomType.choices)


class DeleteReview(forms.Form):
    isDelete = forms.BooleanField(label="Delete post", initial=False, required=False)
    notDelete = forms.BooleanField(label = "Not delete post", initial=False, required=False)


class UpdateForm(forms.Form):
    room_type = forms.ChoiceField(label="Select your room type", choices=Review.RoomType.choices)

