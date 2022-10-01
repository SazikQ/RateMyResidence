from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
# Register your models here.
from .models import User, Review, Residence, Location
from ..user_authentication.forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ("isVerifiedUser", "isResidenceManager")}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Residence)
admin.site.register(Review)
admin.site.register(Location)
