from django.urls import path

from apps.goods.views import ProductsAPIView, ProductAPIView


urlpatterns = [
    path("", ProductsAPIView.as_view(), name="products"),
    path("<int:id>/", ProductAPIView.as_view(), name="product"),
]
