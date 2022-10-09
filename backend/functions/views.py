from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from backend.functions.forms import ResidenceForm
from django.views.generic import TemplateView, ListView, DetailView
from backend.user_profile.models import Residence, Location
from django.urls import reverse
from django.contrib import messages

# Create your views here.

def add_residence(request):
    if request.method == 'POST':
        form = ResidenceForm(request.POST)
        if form.is_valid():
            saved_location = Location(streetName=form.cleaned_data['streetName'], streetNum=form.cleaned_data['streetNum'], zipcode=form.cleaned_data['zipcode'])
            saved_location.save()
            residence = Residence(name=form.cleaned_data['name'], location=saved_location)
            residence.save()
            return HttpResponseRedirect("/")
    else:
        form = ResidenceForm()
    return render(request, 'addResidence.html', {'form': form.as_p()})

def autocomplete(request):
    residences = Residence.objects.all()
    return render(request, 'main.html', {'resnames': residences})


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

class AddResidenceView(DetailView):
    model = Residence
    template_name = 'residence_info.html'
    # fields = '__all__'
    # def index(request):
    #     name = request.name
    #     manager = request.manager
    #     streetName = request.location.streetName
    #     content = {'name': name, 'manager':manager, 'streetName':streetName}
    #     return render(request, 'residence_info.html', content)