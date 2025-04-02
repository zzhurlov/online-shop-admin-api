from django.urls import path

from apps.goods.views import (
    ProductsAPIView,
    ProductAPIView,
    CategoriesAPIView,
    CategoryAPIView,
)


urlpatterns = [
    path("products/", ProductsAPIView.as_view(), name="products"),
    path("products/<int:id>/", ProductAPIView.as_view(), name="product"),
    path(
        "categories/",
        CategoriesAPIView.as_view(),
        name="categories",
    ),
    path("categories/<int:id>/", CategoryAPIView.as_view(), name="category"),
]
