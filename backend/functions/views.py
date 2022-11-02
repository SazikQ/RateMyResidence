from audioop import reverse
import re
from turtle import title
from xml.etree.ElementInclude import default_loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_list_or_404
from backend.functions.forms import ResidenceForm, ReviewForm, EditReview, DeleteReview, ResidenceEditForm, UpdateForm
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from backend.user_profile.models import Residence, Review, Location
from django.db.models import Q, Count
from taggit.forms import *


# Create your views here.
@login_required
def dislike_view(request, pk):
    rev = Review.objects.get(pk=request.GET.get('review_id'))
    redirectUrl = '/residence/' + str(pk)
    if rev.likes.filter(id=request.user.id).exists():
        rev.likes.remove(request.user)
        rev.dislikes.add(request.user)
        return HttpResponseRedirect(redirectUrl)

    if rev.dislikes.filter(id=request.user.id).exists():
        rev.dislikes.remove(request.user)
    else:
        rev.dislikes.add(request.user)
    return HttpResponseRedirect(redirectUrl)


def like_view(request, pk):
    rev = Review.objects.get(pk=request.GET.get('review_id'))
    redirectUrl = '/residence/' + str(pk)
    if rev.dislikes.filter(id=request.user.id).exists():
        rev.dislikes.remove(request.user)
        rev.likes.add(request.user)
        return HttpResponseRedirect(redirectUrl)

    if rev.likes.filter(id=request.user.id).exists():
        rev.likes.remove(request.user)
    else:
        rev.likes.add(request.user)
    return HttpResponseRedirect(redirectUrl)

    # get_list_or_404(Review, id=request.POST.get('review_id'))


def delete_review(request, pk):
    review_form = Review.objects.get(pk=pk)
    residence_info = review_form.belongedResidence
    redirectUrl = "/residence/" + str(residence_info.pk)

    if request.user != review_form.reviewer:
        return HttpResponseRedirect(redirectUrl)

    review_form.delete()
    return HttpResponseRedirect(redirectUrl)

    """
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
    """


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
            review_form.time_lived = form.cleaned_data['time_lived']
            review_form.live_again = form.cleaned_data['live_again']
            review_form.location_rating = form.cleaned_data['location_rating']
            review_form.quality_rating = form.cleaned_data['quality_rating']
            review_form.quietness_rating = form.cleaned_data['quietness_rating']
            review_form.rent = form.cleaned_data['rent']
            review_form.room_type = form.cleaned_data['room_type']
            review_form.save(update_fields=['title'])
            review_form.save(update_fields=['content'])
            review_form.save(update_fields=['isAnonymous'])
            review_form.save(update_fields=['rating'])
            review_form.save(update_fields=['time_lived'])
            review_form.save(update_fields=['live_again'])
            review_form.save(update_fields=['rent'])
            review_form.save(update_fields=['location_rating'])
            review_form.save(update_fields=['quality_rating'])
            review_form.save(update_fields=['quietness_rating'])
            review_form.save(update_fields=['room_type'])
            return HttpResponseRedirect(redirectUrl)
    else:
        if pk == '':
            raise Http404
        request.session['pk'] = pk
        form = EditReview()
    return render(request, 'editreview.html', {'review_form': form.as_p(), 'comment': review_form})


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
                            time_lived=form.cleaned_data['time_lived'], live_again=form.cleaned_data['live_again'],
                            rent=form.cleaned_data['rent'],
                            location_rating=form.cleaned_data['location_rating'],
                            quality_rating=form.cleaned_data['quality_rating'],
                            quietness_rating=form.cleaned_data['quietness_rating'],
                            room_type = form.cleaned_data['room_type'])
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
        order_list = []
        rating_order = self.request.GET.get('ratingRange')
        if (rating_order != "None"):
            order_list.append(rating_order)
        price_order = self.request.GET.get('priceRange')
        if (price_order != "None"):
            order_list.append(price_order)
        minRate = self.request.GET.get('rating_min')
        if (not minRate.isnumeric()):
            minRate = 0
        maxRate = self.request.GET.get('rating_max')
        if (not maxRate.isnumeric()):
            maxRate = 5
        minPrice = self.request.GET.get('price_min')
        if (not minPrice.isnumeric()):
            minPrice = 0
        maxPrice = self.request.GET.get('price_max')
        if (not maxPrice.isnumeric()):
            maxPrice = float('inf')

        if (query == ''):
            messages.info(self.request, ('Please enter a keyword or letter to search for.'))
            self.valid_input = False
            return Residence.objects.exclude(name__icontains=query)
        if order_list:
            object_list = Residence.objects.filter(
                Q(name__icontains=query) &
                Q(rating_average__lte=maxRate) &
                Q(rating_average__gte=minRate) &
                Q(rent_min__lte=maxPrice) &
                Q(rent_max__gte=minPrice)
            ).order_by(*order_list)
            return object_list
        else:
            object_list = Residence.objects.filter(
                Q(name__icontains=query) &
                Q(rating_average__lte=maxRate) &
                Q(rating_average__gte=minRate) &
                Q(rent_min__lte=maxPrice) &
                Q(rent_max__gte=minPrice)
            )
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

    # if request.user != instance.manager:
    # return HttpResponseRedirect(redirectUrl)

    if request.method == 'POST':
        form = ResidenceEditForm(request.POST)
        pk = request.session['pk']
        if pk == '':
            raise Http404
        if form.is_valid():
            instance.location.streetName = form.cleaned_data['streetName']
            instance.location.streetNum = form.cleaned_data['streetNum']
            instance.location.zipcode = form.cleaned_data['zipcode']
            instance.location.save(update_fields=['streetName', 'streetNum', 'zipcode'])
            instance.name = form.cleaned_data['name']
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
        form = ResidenceEditForm({
            'name': instance.name,
            'streetName': instance.location.streetName,
            'streetNum': instance.location.streetNum,
            'zipcode': instance.location.zipcode,
        })
    return render(request, 'editResidence.html', {'form': form.as_p()})


class ResidenceListView(ListView):
    model = Residence
    template_name = 'residence_list.html'
    """
    def post(request):
        if request.method == 'POST':
            form = TagSearch(request.POST)
            if form.is_valid():
                ResidenceListView.get_queryset(request)
        else:
            object_list = Residence.objects.all()
            return render(request,'residence_list.html', {'object_list': object_list})
"""
    def get_queryset(self):
        query = self.request.GET.get('q')
        if (query == '' or query is None):
            object_list = Residence.objects.all()
            return object_list
        else:
            object_list = Residence.objects.filter(tags__name__in=[query])
        #print(object_list)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = ResidenceListView.tagcomplete(self.request)
        context['tagnames'] = tags
        return context

    def tagcomplete(request):
        residences = Residence.objects.all()
        tag_list = []
        for res in residences:
            for tag in res.tags.names():
                if tag not in tag_list:
                    tag_list.append(tag)
        print(tag_list)
        return tag_list




class ResidenceDetail(DetailView):
    model = Residence
    template_name = 'residence_info.html'

    def get(self, request, pk):
        sort = request.GET.get('sort')
        print(sort)
        targetResidence = Residence.objects.get(pk=pk)
        review_list = targetResidence.comments.all()
        tags = targetResidence.tags.names()

        if (sort == 'likes'):
            review_order = review_list.annotate(num_like=Count('likes')).order_by('-num_like')
        elif (sort == 'dislikes'):
            review_order = review_list.annotate(num_dislike=Count('dislikes')).order_by('-num_dislike')
        elif (sort == 'lhratings'):
            review_order = review_list.order_by('rating')
        elif (sort == 'hlratings'):
            review_order = review_list.order_by('-rating')
        else:
            review_order = review_list.order_by('pk')

        context = {'reviews': review_order, 'object': targetResidence, 'tags': tags, 'updateForm': UpdateForm().as_p()}
        return render(request, 'residence_info.html', context)

    def post(self, request, pk):
        if request.method == "POST":
            update_form = UpdateForm(request.POST)
            if update_form.is_valid():
                targetResidence = Residence.objects.get(pk=pk)
                room_type = update_form.cleaned_data['room_type']
                tags = targetResidence.tags.names()
                review_list = Review.objects.filter(belongedResidence=targetResidence, room_type=room_type)
                context = {'reviews': review_list, 'object': targetResidence, 'tags': tags, 'updateForm': UpdateForm().as_p()}
                return render(request, 'residence_info.html', context)
            else:
                return redirect('residence_info', pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        targetResidence = Residence.objects.get(pk=self.object.pk)
        context['tags'] = targetResidence.tags.names()
        context['updateForm'] = UpdateForm().as_p()
        return context
