from django import forms


class ResidenceForm(forms.Form):
    name = forms.CharField(label='Residence name', max_length=100)
    streetName = forms.CharField(max_length=100)
    streetNum = forms.CharField(max_length=20)
    zipcode = forms.CharField(max_length=6)


class ReviewForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(label='Review content', max_length=500)
