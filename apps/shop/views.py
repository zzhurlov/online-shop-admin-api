from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from apps.shop.models import Shop
from apps.shop.serializers import ShopSerializer, CreateShopSerializer
from apps.accounts.permissions import IsSuperUser
from apps.accounts.models import User
from apps.shop.filters import ShopFilter
from apps.shop.schema_examples import SHOP_PARAM_EXAMPLE

from drf_spectacular.utils import extend_schema


class ShopsAPIView(APIView):
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ShopSerializer
        elif self.request.method == "POST":
            return CreateShopSerializer
        return ShopSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]

        elif self.request.method == "POST":
            return [IsSuperUser()]

    @extend_schema(
        operation_id="filtering_shops",
        summary="Search shops by title",
        description="This endpoint allows user to search shops by title (optional)",
        parameters=SHOP_PARAM_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        shops = Shop.objects.prefetch_related("responsible_id").all()

        filterset = ShopFilter(request.query_params, queryset=shops)
        if filterset.is_valid():
            queryset = filterset.qs
            serializer = self.get_serializer_class()(queryset, many=True)
            return Response(data=serializer.data, status=200)
        else:
            return Response(filterset.errors, status=400)

    @extend_schema(
        summary="Add the shop",
        description="This endpoint allows superuser to add the shops",
    )
    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            users_ids = data.pop("responsible_id", None)

            if users_ids and (0 not in set(users_ids)):
                users = User.objects.filter(id__in=users_ids)

                shop = Shop.objects.create(**data)
                shop.responsible_id.set(users)
                shop.save()

                serializer = self.get_serializer_class()(shop)
                return Response(data=serializer.data, status=200)
            return Response(
                data={"message": "You have to add existing responsibles for shop!"},
                status=400,
            )
        return Response(data={"message": "Error, check your details!"}, status=400)


class ShopAPIView(APIView):
    serializer_class = ShopSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]

        elif self.request.method == "PATCH":
            return [IsSuperUser()]

    def get_object(self, id):
        try:
            shop = Shop.objects.get(id=id)
        except Shop.DoesNotExist:
            shop = None
        return shop

    @extend_schema(
        operation_id="shop_detail",
        summary="Retrieve shop detail",
        description="This endpoint allows user to get a shop detail using id",
    )
    def get(self, request, *args, **kwargs):
        shop = self.get_object(id=kwargs["id"])

        if shop is not None:
            serializer = self.serializer_class(shop)
            return Response(data=serializer.data, status=200)

        return Response(data={"message": "Shop with that identifier does not exist!"})

    @extend_schema(
        summary="Change the details of shop",
        description="This endpoint allows superuser to change the shop details",
    )
    def patch(self, request, *args, **kwargs):
        shop = self.get_object(id=kwargs["id"])

        if shop is not None:
            serializer = self.serializer_class(shop, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=200)

            return Response(data={"message": "Error, check your details!"}, status=400)
        return Response(data={"message": "This shop does not exist!"}, status=404)
