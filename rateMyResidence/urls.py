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
from backend.functions.views import ResidenceDetail, SearchResultsView, add_residence, ResidenceListView, add_review, \
    autocomplete, edit_review, delete_review, edit_residence, like_view, dislike_view, UserListView, \
    UniversityResidence, NonUniversityResidence, TopTen, WorstResidenceView, RequestListView, RequestDetailView, \
    user_release_view, user_ban_view, user_promote_view, report_review, report_residence, ReviewDetailView, delete_reply, \
    edit_reply
from django.contrib.auth import views as auth_views
from backend.functions.views import SearchResultsView
from backend.functions.views import add_residence
from backend.user_authentication.views import change_password
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from backend.user_profile.views import profile_photo

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", autocomplete, name="home"),
    path("profile/", include('backend.user_profile.urls')),
    path("accounts/", include("backend.user_authentication.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('list/', ResidenceListView.as_view(), name='list_residence'),
    path('residence/<int:pk>', ResidenceDetail.as_view(), name='residence_info'),
    path('residence/<int:pk>/edit/', edit_residence, name = 'editResidence'),
    path('addResidence/', add_residence, name='add_residence'),
    path('addReview/<str:pk>', add_review, name='add_review'),
    path("profile/password/", change_password, name="changePassword"),
    path("changecomment/<int:pk>/", edit_review, name="changeComment"),
    path("deletecomment/<int:pk>", delete_review, name = "deleteReview"),
    path("residence/like/<int:pk>", like_view, name = "likeReview"),
    path("residence/dislike/<int:pk>", dislike_view, name = "dislikeReview"),
    path('accounts/', include('allauth.urls')),
    path('userlist/', UserListView.as_view(), name ='user_list'),
    path('residence/worstResidence/',WorstResidenceView.as_view() , name='worst_residence'),
    path('university/', UniversityResidence.as_view(), name ='university_list'),
    path('nonuniversity/', NonUniversityResidence.as_view(), name ='nonuniversity_list'),
    path('top10/', TopTen.as_view(), name ='top_ten'),
    path('request_list/', RequestListView.as_view(), name ='request_list'),
    path('request/<int:pk>', RequestDetailView.as_view(), name='request_detail'),
    path('user_promote/<int:pk>', user_promote_view, name='user_promote'),
    path('user_ban/<int:pk>', user_ban_view, name='user_ban'),
    path('user_release/<int:pk>', user_release_view, name='user_release'),
    path("residence/reportReview/<int:pk>", report_review, name = "reportReview"),
    path('residence/reportResidence/<int:pk>', report_residence, name="reportResidence"),
    path('replyReview/<int:pk>/', ReviewDetailView.as_view(), name='replyReview'),
    path('deleteReply/<int:pk>', delete_reply, name='deleteReply'),
    path('changeReply/<int:pk>/', edit_reply, name='changeReply'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

