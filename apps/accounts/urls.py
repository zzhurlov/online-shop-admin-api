from django.urls import path

from apps.accounts.views import (
    RegisterAPIView,
    ProfileAPIView,
    ProfilesAPIView,
    MyProfileAPIView,
)

urlpatterns = [
    path("signup/", RegisterAPIView.as_view(), name="signup"),
    path("profiles", ProfilesAPIView.as_view(), name="profiles"),
    path("profile/<str:email>/", ProfileAPIView.as_view(), name="profile"),
    path("myprofile/", MyProfileAPIView.as_view(), name="myprofile"),
]
