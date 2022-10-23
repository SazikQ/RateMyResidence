from turtle import title
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from backend.functions.forms import ResidenceForm, ReviewForm, EditReview, DeleteReview, ResidenceEditForm
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from backend.user_profile.models import Residence, Review, Location
from taggit.forms import *

# Create your views here.
@login_required
def delete_review(request, pk):
    review_form = Review.objects.get(pk=pk)
    residence_info = review_form.belongedResidence
    redirectUrl = "/residence/" + str(residence_info.pk)

    if request.user != review_form.reviewer:
        return HttpResponseRedirect(redirectUrl)

    if request.method == 'POST':
        form = DeleteReview(request.POST)
        pk = request.session['pk']
        if pk == '':
            raise Http404
        if form.is_valid():
            if form.cleaned_data["isDelete"] == True and form.cleaned_data["notDelete"] == False:
                review_form = Review.objects.get(pk=pk)
                review_form.delete()
                residence_info = review_form.belongedResidence
                redirectUrl = "/residence/" + str(residence_info.pk)
            else:
                review_form = Review.objects.get(pk=pk)
                residence_info = review_form.belongedResidence
                redirectUrl = "/residence/" + str(residence_info.pk)
            return HttpResponseRedirect(redirectUrl)
    else:
        if pk == '':
            raise Http404
        request.session['pk'] = pk
        form = DeleteReview()
    return render(request, 'deletereview.html', {'form': form.as_p()})


def edit_review(request, pk):
    review_form = Review.objects.get(pk=pk)
    residence_info = review_form.belongedResidence
    redirectUrl = "/residence/" + str(residence_info.pk)

    if request.user != review_form.reviewer:
        return HttpResponseRedirect(redirectUrl)

    if request.method == 'POST':
        form = EditReview(request.POST)
        pk = request.session['pk']
        if pk == '':
            raise Http404
        if form.is_valid():
            review_form.title = form.cleaned_data['title']
            review_form.content = form.cleaned_data['content']
            review_form.isAnonymous = form.cleaned_data['isAnonymous']
            review_form.rating = form.cleaned_data['rating']
            review_form.save(update_fields = ['title'])
            review_form.save(update_fields = ['content'])
            review_form.save(update_fields = ['isAnonymous'])
            review_form.save(update_fields = ['rating'])
            return HttpResponseRedirect(redirectUrl)
    else:
        if pk == '':
            raise Http404
        request.session['pk'] = pk
        form = EditReview()
    return render(request, 'editreview.html', {'review_form': form.as_p()})

@login_required
def add_review(request, pk):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        pk = request.session['pk']
        if pk == '':
            raise Http404
        if form.is_valid():
            review = Review(title=form.cleaned_data['title'], content=form.cleaned_data['content'],
                            isAnonymous=form.cleaned_data['isAnonymous'], reviewer=request.user,
                            belongedResidence=Residence.objects.get(pk=pk), rating=form.cleaned_data['rating'],
                            time_lived = form.cleaned_data['time_lived'], live_again = form.cleaned_data['live_again'],
                            rent = form.cleaned_data['rent'])
            review.save()
            redirectUrl = "/residence/" + pk
            return HttpResponseRedirect(redirectUrl)
    else:
        if pk == '':
            raise Http404
        request.session['pk'] = pk
        form = ReviewForm()
    return render(request, 'addReview.html', {'form': form.as_p()})


def add_residence(request):
    if request.method == 'POST':
        form = ResidenceForm(request.POST)
        if form.is_valid():
            saved_location = Location(streetName=form.cleaned_data['streetName'],
                                      streetNum=form.cleaned_data['streetNum'], zipcode=form.cleaned_data['zipcode'])
            saved_location.save()
            residence = Residence(name=form.cleaned_data['name'], location=saved_location)
            residence.save()
            m_tags = form.cleaned_data['residence_tags']
            for m_tag in m_tags:
                residence.tags.add(m_tag)
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


def edit_residence(request, pk):
    instance = Residence.objects.get(pk=pk)
    redirectUrl = "/residence/" + str(pk)

    #if request.user != instance.manager:
        #return HttpResponseRedirect(redirectUrl)

    if request.method == 'POST':
        form = ResidenceEditForm(request.POST)
        pk = request.session['pk']
        if pk == '':
            raise Http404
        if form.is_valid():
            instance.location.streetName=form.cleaned_data['streetName']
            instance.location.streetNum=form.cleaned_data['streetNum']
            instance.location.zipcode=form.cleaned_data['zipcode']
            instance.location.save(update_fields=['streetName', 'streetNum', 'zipcode'])
            instance.name=form.cleaned_data['name']
            instance.save(update_fields=['name'])
            instance.tags.clear()
            m_tags = form.cleaned_data['residence_tags']
            for m_tag in m_tags:
                instance.tags.add(m_tag)
            instance.save()

            return HttpResponseRedirect(redirectUrl)
    else:
        if pk == '':
            raise Http404
        request.session['pk'] = pk
        form = ResidenceEditForm()
    return render(request, 'editResidence.html', {'form': form.as_p()})

class ResidenceListView(ListView):
    model = Residence
    template_name = 'residence_list.html'


class ResidenceDetail(DetailView):
    model = Residence
    template_name = 'residence_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        targetResidence = Residence.objects.get(pk=self.object.pk)
        context['tags'] = targetResidence.tags.names()
        return context