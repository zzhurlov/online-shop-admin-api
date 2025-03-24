from django.urls import path

from apps.accounts.views import RegisterAPIView

urlpatterns = [
    path("signup/", RegisterAPIView.as_view(), name="signup"),
]
