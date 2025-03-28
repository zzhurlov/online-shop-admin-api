from django.urls import path

from apps.shop.views import ShopAPIView, ShopsAPIView


urlpatterns = [
    path("<int:id>/", ShopAPIView.as_view(), name="shop"),
    path("", ShopsAPIView.as_view(), name="shops"),
]
