from django.contrib import admin

# Register your models here.
from.models import User
from.models import Review
from .models import Residence
from .models import Location


admin.site.register(User)
admin.site.register(Residence)
admin.site.register(Review)
admin.site.register(Location)
