import django_filters

from apps.goods.models import ShopProduct, Category


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="product__title", lookup_expr="icontains"
    )
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")

    class Meta:
        model = ShopProduct
        fields = ["max_price", "min_price"]


class CategoryFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    parent_title = django_filters.CharFilter(
        field_name="parent__title", lookup_expr="icontains"
    )

    class Meta:
        model = Category
        fields = ["title"]
