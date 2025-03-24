from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from apps.accounts.permissions import IsSuperUser
from apps.accounts.serializers import CreateUserSerializer, ProfileSerializer
from apps.accounts.models import User
from apps.accounts.utils import set_dict_attr

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


class ProfileAPIView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsSuperUser]

    def get_object(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        return user

    def get(self, request, *args, **kwargs):
        user = self.get_object(kwargs["email"])

        if user is not None:
            serializer = self.serializer_class(user)
            return Response(data=serializer.data, status=200)
        return Response(data={"message": "This User does not exist!"})

    def patch(self, request, *args, **kwargs):
        user = self.get_object(kwargs["email"])

        if user is not None:
            serializer = self.serializer_class(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=200)
            return Response(data={"message": "Error, Check your details!"}, status=400)

        return Response(data={"message": "This user does not exist!"})

    def delete(self, request, *args, **kwargs):
        user = self.get_object(kwargs["email"])

        if user is not None:
            user.delete()
            return Response(data={"message": "This user has deleted successfully!"})
        return Response(data={"message": "This user does not exist!"})


class ProfilesAPIView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsSuperUser]

    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(data=serializer.data, status=200)


class MyProfileAPIView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(data=serializer.data, status=200)

    def patch(self, request):
        user = request.user

        if user.is_active:
            serializer = self.serializer_class(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=200)
            return Response(data={"message": "Check your details!"}, status=400)

        return Response(
            data={"message": "You don't have permission to do this!"}, status=403
        )
