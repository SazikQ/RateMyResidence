from django.urls import path
from . import views
#from .views import EditProfileView
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.profile, name = "profile"),
    path('edit/', views.edit_profile, name = "editProfile")
]