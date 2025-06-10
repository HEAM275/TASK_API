
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# models and serializers
from apps.users.serializer.user_serializer import *
from apps.users.models import User

# viewser base
from apps.base.views import BaseModelViewSet


class UserViewSet(BaseModelViewSet):
    """
    API endpoints for managment of users
    """

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserListSerializer
        if self.action in ['create']:
            return UserCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserListSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    swagger_auto_schema(
        operation_description='list of active users.',
        responses={
            200: UserListSerializer,
            404: _('You dont have acces to this information.')
        }
    )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    swagger_auto_schema(
        operation_description='list of a especific user.',
        responses={
            200: UserListSerializer,
            403: _('The user is not active or does not exist.'),
            404: _('You dont have acces to this information.')
        }
    )

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    swagger_auto_schema(
        operation_description='create a new user.',
        request_body=UserCreateSerializer,
        responses={
            201: _('User created successfully'),
            400: _('You have to fill all the fields or the user do you want to create is already in the database.'),
            403: _('You dont have acces to this information.'),
        }
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'user created successfully ', "data": serializer.data},
                status=status.HTTP_201_CREATED)
        return Response({'message': 'user could not be created', 'error': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    swagger_auto_schema(
        operation_description='update a user.',
        request_body=UserUpdateSerializer,
        responses={
            200: _('User updated successfully'),
            400: _('Invalid data'),
            403: _('You dont have acces to this information.'),
            404: _('The user does not exist.')
        }
    )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'user updated successfully ', "data": serializer.data},
                status=status.HTTP_200_OK)
        return Response({'message': 'user could not be updated', 'error': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    swagger_auto_schema(
        operation_description='delete a user (is_active = false).',
        responses={
            200: _('User deleted successfully'),
            403: _('You dont have acces to this information.'),
            404: _('The user does not exist.')
        }
    )

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
