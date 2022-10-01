from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from backend.functions.forms import SearchForm


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
