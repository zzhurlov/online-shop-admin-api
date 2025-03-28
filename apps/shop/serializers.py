from rest_framework import serializers

from apps.shop.models import Shop
from apps.accounts.serializers import ResponsibleSerializer


class ShopSerializer(serializers.ModelSerializer):
    responsible_id = ResponsibleSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = "__all__"


class CreateShopSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=30)
    desc = serializers.CharField(max_length=1000)
    responsible_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    is_active = serializers.BooleanField(default=True)
    image = serializers.ImageField(required=False)
