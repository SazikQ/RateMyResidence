from django.contrib import admin

# Register your models here.
from.models import User
from.models import Review
from .models import Residence

admin.site.register(User)
admin.site.register(Residence)
admin.site.register(Review)
