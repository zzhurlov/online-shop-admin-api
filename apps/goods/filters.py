import django_filters

from apps.goods.models import ShopProduct


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="product__title", lookup_expr="icontains"
    )
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")

    class Meta:
        model = ShopProduct
        fields = ["max_price", "min_price"]
