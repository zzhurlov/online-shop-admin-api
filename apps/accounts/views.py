from rest_framework.views import APIView
from rest_framework.response import Response

from apps.accounts.permissions import IsSuperUser
from apps.accounts.serializers import CreateUserSerializer
from apps.accounts.models import User

from drf_spectacular.utils import extend_schema


class RegisterAPIView(APIView):
    serializer_class = CreateUserSerializer
    permission_classes = [IsSuperUser]

    @extend_schema(
        summary="Registration",
        description="This endpoint allows superuser to create the responsibles and superusers",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            new_user = User.objects.create(**data)
            new_user.set_password(data["password"])
            new_user.save()

            return Response(
                data={"message": "You've registered successfully!"}, status=200
            )

        return Response(
            data={"message": "Check your details, maybe your email already exists"},
            status=400,
        )
