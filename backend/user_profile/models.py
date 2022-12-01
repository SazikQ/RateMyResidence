from email.policy import default
from pyexpat import model
from random import choices
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _
# Create your models here.


class User(AbstractUser):
    isVerifiedUser = models.BooleanField(default=False)
    requestManager = models.BooleanField(default=False)
    isPurdueVerified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.isVerifiedUser = True
            self.is_active = True
        if self.email.__contains__("@purdue.edu"):
            self.isPurdueVerified = True
        super(User, self).save(*args, **kwargs)

class Location(models.Model):
    streetName = models.CharField(max_length=100)
    streetNum = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=6)


class Residence(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ManyToManyField(User)
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True)
    distance = models.FloatField(default=0)
    university = models.BooleanField(default=False)
    website = models.CharField(max_length= 150, default="None")
    rating_average = models.FloatField(default=0)
    rent_average = models.FloatField(default=0)
    rent_min = models.FloatField(default=0)
    rent_max = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)
    isReported = models.ManyToManyField(User, related_name='report_residence', blank=True)
    
    class ParkingPolicy(models.TextChoices):
        NOPARK = 'NP', _('No Parking')
        PAIDPARK = 'PP', _('Paid Parking')
        RESPARK = 'RP', _('Reserved Parking')
        INCPARK = 'IP', _('Included Parking')
        CUSTPARK = 'OP', _('Other')
        UNKNOWN = 'UN', _('Unknown')

    parking_policy = models.CharField(
        max_length=2,
        choices=ParkingPolicy.choices,
        default=ParkingPolicy.UNKNOWN,
    )

    class PetPolicy(models.TextChoices):
        NOPETS = 'NP', _('No Pets')
        RESPETS = 'RP', _('Restricted Pets')
        RENTPETS = 'PP', _('Increased Rent')
        CUSTPARK = 'OP', _('Other')
        UNKNOWN = 'UN', _('Unknown')

    pet_policy = models.CharField(
        max_length=2,
        choices=PetPolicy.choices,
        default=PetPolicy.UNKNOWN,
    )

    tags = TaggableManager()

    def __str__(self):
        return self.name

    def update_review_fields(self):
        reviews = self.comments.all()
        #reviews = Review.objects.filter(id=self.id)
        self.rating_average = reviews.aggregate(models.Avg('rating')).get('rating__avg')
        self.rent_average = reviews.aggregate(models.Avg('rent')).get('rent__avg')
        self.rent_min = reviews.aggregate(models.Min('rent')).get('rent__min')
        self.rent_max = reviews.aggregate(models.Max('rent')).get('rent__max')
        self.review_count = reviews.count()
        self.save(update_fields=['rating_average', 'rent_average','rent_min','rent_max','review_count'])

class Review(models.Model):
    publishTime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    isAnonymous = models.BooleanField(default=False)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    belongedResidence = models.ForeignKey(Residence, related_name='comments', on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    time_lived = models.IntegerField(default=0)
    live_again = models.BooleanField(default=False)
    rent = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_user', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_user', blank=True)
    quietness_rating = models.FloatField(default=0)
    location_rating = models.FloatField(default=0)
    quality_rating = models.FloatField(default=0)
    has_furniture = models.BooleanField(default=False)
    isReported = models.ManyToManyField(User, related_name='report_review', blank=True)

    class RoomType(models.TextChoices):
        STUDIO = 'ST', _('Studio')
        SHAREDROOM = 'SH', _('Shared-room')
        TWOROOM = 'TO', _('Two-room')
        THREEROOM = 'TH', _('Three-room')
        FOURROOM = 'FR', _('Four-room')
        UNKNOWN = 'UN', _('Unknown')

    room_type = models.CharField(
        max_length=2,
        choices=RoomType.choices,
        default=RoomType.UNKNOWN,
    )

    class Meta:
        ordering = ['publishTime']
    
    def __str__(self):
        # return super().__str__()
            return '%s - %s' % (self.belongedResidence.name, self.reviewer)
    
    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        self.belongedResidence.update_review_fields()

class Reply(models.Model):
    publishTime = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=500)
    replier = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, related_name='replies',on_delete=models.CASCADE)


class ReviewImage(models.Model):
    photo = models.ImageField(upload_to='review_media')
    belonged_review = models.ForeignKey(Review, related_name='review_image', on_delete=models.CASCADE)


class ProfileImage(models.Model):
    photo = models.ImageField(upload_to='user_media')
    belonged_user = models.ForeignKey(User, related_name='profile_image', on_delete=models.CASCADE)


class ResidenceImage(models.Model):
    photo = models.ImageField(upload_to='residence_media')
    belonged_residence = models.ForeignKey(Residence, related_name='residence_image', on_delete=models.CASCADE)


class ResidenceRequest(models.Model):
    requestResidence = models.ForeignKey(Residence, related_name='residence_request', on_delete=models.CASCADE)
    belonged_user = models.ForeignKey(User, related_name='manager_request', on_delete=models.CASCADE)


class RequestFile(models.Model):
    file = models.FileField(upload_to='request_file')
    belonged_request = models.ForeignKey(ResidenceRequest, related_name='request_file', on_delete=models.CASCADE)