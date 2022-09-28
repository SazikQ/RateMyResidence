from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    isVerifiedUser = models.BooleanField
    isResidenceManager = models.BooleanField


class Residence(models.Model):
    residenceName = models.CharField(max_length=100)
    residenceManager = models.ForeignKey(User)

class Review(models.Model):
    reviewTitle = models.CharField(max_length=100)
    reviewContent = models.CharField(max_length=10000)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewedResidence = models.ForeignKey(Residence, on_delete=models.CASCADE)


