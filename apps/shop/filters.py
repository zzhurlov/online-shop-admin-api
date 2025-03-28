import django_filters

from apps.shop.models import Shop


class ShopFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Shop
        fields = ["title"]
