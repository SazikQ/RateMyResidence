from turtle import title
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from backend.functions.forms import ResidenceForm, ReviewForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from backend.user_profile.models import Residence, Location, Review
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.
@login_required
def add_residence(request):
    if request.method == 'POST':
        form = ResidenceForm(request.POST)
        if form.is_valid():
            saved_location = Location(streetName=form.cleaned_data['streetName'],
                                      streetNum=form.cleaned_data['streetNum'], zipcode=form.cleaned_data['zipcode'])
            saved_location.save()
            residence = Residence(name=form.cleaned_data['name'], location=saved_location)
            residence.save()
            return HttpResponseRedirect("/")
    else:
        form = ResidenceForm()
    return render(request, 'addResidence.html', {'form': form.as_p()})


class SearchResultsView(ListView):
    allow_empty = False
    model = Residence
    template_name = 'residence_list.html'
    valid_input = True

    def get_queryset(self):
        query = self.request.GET.get('q')
        if (query == ''):
            messages.info(self.request, ('Please enter a keyword or letter to search for.'))
            self.valid_input = False
            return Residence.objects.exclude(name__icontains=query)
        else:
            object_list = Residence.objects.filter(name__icontains=query)
            return object_list

    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except Http404:
            if (self.valid_input):
                messages.error(self.request, ('There are no residences that match your search request!'))
            return redirect("/")


class ResidenceListView(ListView):
    model = Residence
    template_name = 'residence_list.html'

class ResidenceDetail(DetailView):
    model = Residence
    template_name = 'residence_info.html'

class AddReview(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'addReview.html'
    # fields = '__all__'

    def add_review(self):
        if self.method == 'POST':
            form = ReviewForm(self.POST)
            if form.is_valid():
                review = Review(title=form.cleaned_data['title'], content=form.cleaned_data['content'])
                review.save()
                return HttpResponseRedirect("/")
        else:
            form = ReviewForm()
        return render(self, 'addReview.html', {'form': form.as_p()})