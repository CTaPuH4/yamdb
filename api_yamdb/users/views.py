from django.core.mail import send_mail
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.mixins import NoPutModelViewSet
from users.permissions import IsAdminOnly
from users.serializers import (User, UserCreateSerializer, UserMeSerializers,
                               UserPatchSerializers, UserSerializer,
                               UserTokenSerializers)

from .constants import PROFILE_ENDPOINT_NAME


class CreateViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    pass


class UserCreateViewSet(CreateViewSet):
    permission_classes = []
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
        )
        confirmation_code = user.get_confirmation_code()
        send_mail(
            subject='YaMDB confirmation_code',
            from_email=None,
            message=f'Confirmation_code: {confirmation_code}',
            recipient_list=[serializer.validated_data.get('email')],
            fail_silently=True,
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_200_OK,
                        headers=headers)


class UserViewSet(NoPutModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.action == 'profile_name' and self.request.method == 'PATCH':
            return UserMeSerializers
        if self.action == 'update':
            return UserPatchSerializers
        return UserSerializer

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated],
            url_path=PROFILE_ENDPOINT_NAME)
    def profile_name(self, request):
        user = request.user
        serializer_class = self.get_serializer_class()
        if request.method == 'PATCH':
            serializer = serializer_class(user,
                                          data=request.data,
                                          partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = serializer_class(user)
        return Response(serializer.data)


class UserTokenViewSet(CreateViewSet):
    permission_classes = []
    serializer_class = UserTokenSerializers
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = User.objects.get(username=username)
        token = user.get_tokens_for_user()
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'token': token},
            status=status.HTTP_200_OK,
            headers=headers)
