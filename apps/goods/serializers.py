from rest_framework import serializers

from apps.goods.models import ShopProduct, Product, Category
from apps.shop.models import Shop
from apps.shop.serializers import ShopSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["shops"]


class ShopProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    shop = ShopSerializer()

    class Meta:
        model = ShopProduct
        fields = "__all__"

    def update(self, instance, validated_data):
        product_data = validated_data.pop("product", None)
        shop_data = validated_data.pop("shop", None)

        if product_data:
            for attr, value in product_data.items():
                setattr(instance.product, attr, value)
            instance.product.save()

        if shop_data:
            for attr, value in shop_data.items():
                setattr(instance.shop, attr, value)
            instance.shop.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class CreateShopProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(), write_only=True
    )

    class Meta:
        model = ShopProduct
        fields = "__all__"

    def create(self, validated_data):
        product_data = validated_data.pop("product")
        shop_data = validated_data.pop("shop")

        product = Product.objects.create(**product_data)

        shopproduct = ShopProduct.objects.create(
            shop=shop_data, product=product, **validated_data
        )

        return shopproduct


class CategorySerializer(serializers.ModelSerializer):
    full_path = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    def get_full_path(self, obj):
        return obj.get_full_path()
