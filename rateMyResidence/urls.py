"""rateMyResidence URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from backend.functions.views import ResidenceDetail, SearchResultsView, add_residence, ResidenceListView, add_review, autocomplete, edit_profile, delete_review, edit_residence
from django.contrib.auth import views as auth_views
from backend.functions.views import SearchResultsView
from backend.functions.views import add_residence
from backend.user_authentication.views import change_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", autocomplete, name="home"),
    path("profile/", include('backend.user_profile.urls')),
    path("accounts/", include("backend.user_authentication.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('list/', ResidenceListView.as_view(), name = 'list_residence'),
    path('residence/<int:pk>', ResidenceDetail.as_view(), name='residence_info'),
    path('residence/<int:pk>/edit/', edit_residence, name = 'editResidence'),
    path('addResidence/', add_residence, name='add_residence'),
    path('addReview/<str:pk>', add_review, name='add_review'),
    path("profile/password/", change_password, name="changePassword"),
    path("changecomment/<int:pk>/", edit_profile, name="changeComment"),
    path("deletecomment/<int:pk>", delete_review, name = "deleteReview")
]
