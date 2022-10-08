from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
#from backend.functions.forms import SearchForm
from backend.user_profile.models import *
from django.views.generic import TemplateView, ListView

# Create your views here.

def search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("hello")
            return HttpResponse("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'name.html', {'form': form})

class SearchResultsView(ListView):
    model = Residence
    template_name = 'residence_temp.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Residence.objects.filter(name__icontains=query)