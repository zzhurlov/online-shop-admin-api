from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from apps.goods.serializers import (
    ShopProductSerializer,
    CategorySerializer,
    CreateShopProductSerializer,
)
from apps.goods.models import ShopProduct, Category
from apps.goods.schema_examples import PRODUCT_PARAM_EXAMPLE, CATEGORY_PARAM_EXAMPLE
from apps.goods.filters import CategoryFilter, ProductFilter

from drf_spectacular.utils import extend_schema


class ProductsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ShopProductSerializer
        elif self.request.method == "POST":
            return CreateShopProductSerializer

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
            serializer = self.get_serializer_class()(queryset, many=True)
            return Response(data=serializer.data, status=200)
        return Response(filterset.errors, status=400)

    @extend_schema(
        summary="Create the new product",
        description="This endpoint allows user to create the new product",
    )
    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)

        if serializer.is_valid():
            shopproduct = serializer.save()

            serializer = self.get_serializer_class()(shopproduct)

            return Response(data=serializer.data, status=200)

        return Response(
            data={"message": "Error, check your details!", "errors": serializer.errors},
            status=400,
        )


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
        operation_id="get_categories_by_title_and_parent_title",
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

    @extend_schema(
        summary="Create the new category",
        description="This endpoint allows user to create the new category",
    )
    def post(self, reqeust):
        serializer = self.serializer_class(data=reqeust.data)

        if serializer.is_valid():
            category = serializer.save()

            serializer = self.serializer_class(category)

            return Response(data=serializer.data, status=200)

        return Response(data={"errors": serializer.errors})


class CategoryAPIView(APIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            category = None

        return category

    @extend_schema(
        operation_id="get_category_by_id",
        summary="Retrieve the category by id",
        description="This endpoint allows user to retrieve the category by id",
    )
    def get(self, request, *args, **kwargs):
        category = self.get_object(id=kwargs["id"])

        if category:
            serializer = self.serializer_class(category)
            return Response(data=serializer.data, status=200)
        return Response(data={"message": "This category does not exist!"}, status=404)
