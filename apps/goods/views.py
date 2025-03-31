from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from apps.goods.serializers import ShopProductSerializer, CategorySerializer
from apps.goods.models import ShopProduct, Category
from apps.goods.schema_examples import PRODUCT_PARAM_EXAMPLE, CATEGORY_PARAM_EXAMPLE
from apps.goods.filters import CategoryFilter, ProductFilter

from drf_spectacular.utils import extend_schema


# TODO: make the POST method for products
class ProductsAPIView(APIView):
    serializer_class = ShopProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        operation_id="filtering_products",
        summary="Get products between max_price and min_price",
        description="This endpoint allows user to get products between max_price and min_price",
        parameters=PRODUCT_PARAM_EXAMPLE,
    )
    def get(self, request):
        products = ShopProduct.objects.select_related("product", "shop").all()

        filterset = ProductFilter(request.query_params, queryset=products)
        if filterset.is_valid():
            queryset = filterset.qs
            serializer = self.serializer_class(queryset, many=True)
            return Response(data=serializer.data, status=200)
        return Response(filterset.errors, status=400)


class ProductAPIView(APIView):
    serializer_class = ShopProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            shopproduct = ShopProduct.objects.get(product__id__exact=id)
        except ShopProduct.DoesNotExist:
            shopproduct = None

        return shopproduct

    @extend_schema(
        operation_id="retrieve_products",
        summary="Get product by id",
        description="This endpoint allows user to get product by id",
    )
    def get(self, request, *args, **kwargs):
        shopproduct = self.get_object(kwargs["id"])

        if shopproduct:
            serializer = self.serializer_class(shopproduct)
            return Response(data=serializer.data, status=200)

        return Response(data={"message": "This product does not exist!"})

    @extend_schema(
        summary="Change the product",
        description="This endpoint allows user to change the product",
    )
    def patch(self, request, *args, **kwargs):
        shopproduct = self.get_object(kwargs["id"])

        if shopproduct:
            serializer = self.serializer_class(
                shopproduct, data=request.data, partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=200)

            return Response(data={"message": "Error, check your details!"}, status=400)

        return Response(data={"message": "This product does not exist!"}, status=400)


class CategoriesAPIView(APIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Retrieve the categories",
        description="This endpoint allows user to retrieve the categories",
        parameters=CATEGORY_PARAM_EXAMPLE,
    )
    def get(self, request):
        categories = Category.objects.select_related("parent").all()

        filterset = CategoryFilter(request.query_params, queryset=categories)
        if filterset.is_valid():
            queryset = filterset.qs
            serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=200)


class CategoryAPIView(APIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            category = None

        return category

    def get(self, request, *args, **kwargs):
        category = self.get_object(id=kwargs["id"])

        if category:
            serializer = self.serializer_class(category)
            return Response(data=serializer.data, status=200)
        return Response(data={"message": "This category does not exist!"}, status=404)
