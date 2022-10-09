from backend.user_profile.models import Review, Residence, User
from django.contrib.auth.models import User

# Testing Return Functions
from backend.user_profile.models import *


def residence_by_name(name):
    return Residence.objects.filter(name__icontains=name)

