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
from backend.user_profile.models import Residence, Review, Location, User, ResidenceImage, ReviewImage
from django.db.models import Q, Count, Min
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

@login_required
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

@login_required
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

@login_required
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
            review_form.has_furniture = form.cleaned_data['has_furniture']
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
            review_form.save(update_fields=['has_furniture'])
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
                            room_type = form.cleaned_data['room_type'],
                            has_furniture= form.cleaned_data['has_furniture'])
            review.save()
            images = request.FILES.getlist('review_photo')
            for image in images:
                ReviewImage.objects.create(photo=image, belonged_review=review)
            redirectUrl = "/residence/" + pk
            return HttpResponseRedirect(redirectUrl)
    else:
        if pk == '':
            raise Http404
        request.session['pk'] = pk
        form = ReviewForm()
    return render(request, 'addReview.html', {'form': form.as_p()})

@login_required
def add_residence(request):
    if request.method == 'POST':
        form = ResidenceForm(request.POST)
        if form.is_valid():
            saved_location = Location(streetName=form.cleaned_data['streetName'],
                                      streetNum=form.cleaned_data['streetNum'], zipcode=form.cleaned_data['zipcode'])
            saved_location.save()
            residence = Residence(
                name=form.cleaned_data['name'], 
                distance=form.cleaned_data['distance'], 
                location=saved_location, 
                parking_policy=form.cleaned_data['parking_policy'], 
                pet_policy=form.cleaned_data['pet_policy'],
                university=form.cleaned_data['university'])
            residence.save()
            m_tags = form.cleaned_data['residence_tags']
            for m_tag in m_tags:
                residence.tags.add(m_tag)
            residence.save()
            images = request.FILES.getlist('residence_photo')
            for image in images:
                ResidenceImage.objects.create(photo=image, belonged_residence=residence)
            return HttpResponseRedirect("/")
    else:
        form = ResidenceForm()
    return render(request, 'addResidence.html', {'form': form.as_p()})

def autocomplete(request):
    residences = Residence.objects.all()
    return render(request, 'main.html', {'resnames': residences})


class SearchResultsView(ListView):
    allow_empty = True
    model = Residence
    template_name = 'residence_list.html'
    valid_input = True

    def get_queryset(self):
        q_objects = Q()
        # Process user input
        name = self.request.GET.get('name')
        if (name and name != ''):
            q_objects &= Q(name__icontains=name)
        """ 
        # Block blank searches
        if (name == ''):
            messages.info(self.request, ('Please enter a keyword or letter to search for.'))
            self.valid_input = False
            return Residence.objects.exclude(name__icontains=name)
        """
        order = self.request.GET.get('OrderBy')
        tags = self.request.GET.get('tag')
        if (tags and tags != ''):
            q_objects &= Q(tags__name__in=[tags])
        order_type = self.request.GET.get('OrderType')
       
        # Set up query parameters
        if (order_type is None or order_type == "None"):
            order = "None"
        if (order and order != "None" and order_type == "-"):
            order = order_type + order
        minRate = self.request.GET.get('rating_min')
        if (minRate and minRate.isnumeric()):
            q_objects &= Q(rating_average__gte=minRate)
        maxRate = self.request.GET.get('rating_max')
        if (maxRate and maxRate.isnumeric()):
            q_objects &= Q(rating_average__lte=maxRate)
        minPrice = self.request.GET.get('price_min')
        if (minPrice and minPrice.isnumeric()):
            q_objects &= Q(rent_max__gte=minPrice)
        maxPrice = self.request.GET.get('price_max')
        if (maxPrice and maxPrice.isnumeric()):
            q_objects &= Q(rent_min__lte=maxPrice)
        minDist = self.request.GET.get('dist_min')
        if (minDist and minDist.isnumeric()):
            q_objects &= Q(distance__gte=minDist)
        maxDist = self.request.GET.get('dist_max')
        if (maxDist and maxDist.isnumeric()):
            q_objects &= Q(distance__lte=maxDist)
        parkPol = self.request.GET.get('ParkingPolicy')
        if (parkPol and parkPol != 'None'):
            q_objects &= Q(parking_policy=parkPol)
        petPol = self.request.GET.get('PetPolicy')
        if (petPol and petPol != 'None'):
            q_objects &= Q(pet_policy=petPol)
        floorPlan = self.request.GET.get('FloorPlan')
        if (floorPlan and floorPlan != 'None'):
            valid = Review.objects.filter(room_type=floorPlan)
            q_objects &= Q(comments__in=valid)
        
        if (order and order != "None"):
            return Residence.objects.filter(q_objects).order_by(order)
        # Conduct query without order
        else:
            return Residence.objects.filter(q_objects)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = SearchResultsView.tagcomplete(self.request)
        res = SearchResultsView.rescomplete(self.request)
        name = self.request.GET.get('name')
        if name:
            context['search_name'] = name
        tag = self.request.GET.get('tag')
        if tag:
            context['tag_name'] = tag
        minPrice = self.request.GET.get('price_min')
        if minPrice:
            context['minPrice'] = minPrice
        maxPrice = self.request.GET.get('price_max')
        if maxPrice:
            context['maxPrice'] = maxPrice
        minRating = self.request.GET.get('rating_min')
        if minRating:
            context['minRating'] = minRating
        maxRating = self.request.GET.get('rating_max')
        if maxRating:
            context['maxRating'] = maxRating
        minDist = self.request.GET.get('dist_min')
        if minDist:
            context['minDist'] = minDist
        maxDist = self.request.GET.get('dist_max')
        if maxDist:
            context['maxDist'] = maxDist
        orderBy = self.request.GET.get('OrderBy')
        if orderBy:
            context['orderByVal'] = orderBy
        orderType = self.request.GET.get('OrderType')
        if orderType:
            context['orderTypeVal'] = orderType
        petPolicy = self.request.GET.get('PetPolicy')
        if petPolicy:
            context['petPolicyVal'] = petPolicy
        parkingPolicy = self.request.GET.get('ParkingPolicy')
        if parkingPolicy:
            context['parkingPolicyVal'] = parkingPolicy
        floorPlan = self.request.GET.get('FloorPlan')
        if floorPlan:
            context['floorPlanVal'] = floorPlan
        
        context['tagnames'] = tags
        context['resnames'] = res
        return context

    def tagcomplete(request):
        residences = Residence.objects.all()
        tag_list = []
        for res in residences:
            for tag in res.tags.names():
                if tag not in tag_list:
                    tag_list.append(tag)
        return tag_list
    
    def rescomplete(request):
        residences = Residence.objects.all()
        res_list = []
        for res in residences:
            res_list.append(res.name)
        return residences

@login_required
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
            instance.website = form.cleaned_data['website']
            instance.save(update_fields=['website'])
            instance.parking_policy = form.cleaned_data['parking_policy']
            instance.save(update_fields=['parking_policy'])
            instance.pet_policy = form.cleaned_data['pet_policy']
            instance.save(update_fields=['pet_policy'])
            instance.university = form.cleaned_data['university']
            instance.save(update_fields=['university'])
            instance.distance = form.cleaned_data['distance']
            instance.save(update_fields=['distance'])
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
        tags_list = ""
        for names in instance.tags.names():
            tags_list += names
            tags_list += ","
        tags_list = tags_list[:-1]
        
        form = ResidenceEditForm({
            'name': instance.name,
            'streetName': instance.location.streetName,
            'streetNum': instance.location.streetNum,
            'zipcode': instance.location.zipcode,
            'distance': instance.distance,
            'website': instance.website,
            'parking_policy': instance.parking_policy,
            'pet_policy': instance.pet_policy,
            'residence_tags': tags_list
        })
    return render(request, 'editResidence.html', {'form': form.as_p()})


class ResidenceListView(ListView):
    model = Residence
    template_name = 'residence_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = SearchResultsView.tagcomplete(self.request)
        res = SearchResultsView.rescomplete(self.request)
        context['tagnames'] = tags
        context['resnames'] = res
        return context

    def tagcomplete(request):
        residences = Residence.objects.all()
        tag_list = []
        for res in residences:
            for tag in res.tags.names():
                if tag not in tag_list:
                    tag_list.append(tag)
        return tag_list
    
    def rescomplete(request):
        residences = Residence.objects.all()
        res_list = []
        for res in residences:
            res_list.append(res.name)
        return residences




class ResidenceDetail(DetailView):
    model = Residence
    template_name = 'residence_info.html'

    def get(self, request, pk):
        sort = request.GET.get('sort')
        #print(sort)
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


class UserListView(ListView):
    model = User
    template_name = "user_list.html"

    def get_queryset(self):
        object_list = User.objects.filter(is_superuser=False)
        return object_list

class WorstResidenceView(ListView):
    model = Residence
    template_name = "worstResidence.html"

    def get_queryset(self):
        residence_list = Residence.objects.all()
        if (residence_list.count != 0):
            lowest_rating = residence_list.aggregate(Min('rating_average'))
            worst_rec = residence_list.filter(rating_average = lowest_rating['rating_average__min'])
            print(worst_rec)
            return worst_rec
        else:
            return residence_list

class UniversityResidence(ListView):
    model = Residence
    template_name = 'university_list.html'
    def get_queryset(self):
        object_list = Residence.objects.filter(university=True)
        return object_list

class NonUniversityResidence(ListView):
    model = Residence
    template_name = 'nonuniversity_list.html'

    def get_queryset(self):
        object_list = Residence.objects.filter(university=False)
        return object_list


class TopTen(ListView):
    model = Residence
    template_name = 'top_ten.html'

    def get_queryset(self):
        object_list = Residence.objects.order_by('-rating_average')
        print("before: ", object_list)
        object_list = object_list[:10]
        print(object_list)
        return object_list

