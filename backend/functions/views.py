from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from backend.functions.forms import ResidenceForm
from django.views.generic import TemplateView, ListView, CreateView
from backend.user_profile.models import Residence, Location


# Create your views here.

def add_residence(request):
    if request.method == 'POST':
        form = ResidenceForm(request.POST)
        if form.is_valid():
            saved_location = Location(streetName=form.cleaned_data['streetName'], streetNum=form.cleaned_data['streetNum'], zipcode=form.cleaned_data['zipcode'])
            saved_location.save()
            residence = Residence(name=form.cleaned_data['name'], location=saved_location)
            residence.save()
            return HttpResponse('thanks')
    else:
        form = ResidenceForm()
    return render(request, 'addResidence.html', {'form': form.as_p()})


class SearchResultsView(ListView):
    model = Residence
    template_name = 'residence_temp.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Residence.objects.filter(name__icontains=query)
        return object_list

class AddResidenceView(CreateView):
    model = Residence
    template_name: str = 'residence_temp.html'
    fields = '__all__'