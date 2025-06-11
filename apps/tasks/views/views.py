# Create your views here

# Django imports
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

# DRF imports
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated

# Swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# API imports
from apps.base.views import BaseModelViewSet
from apps.tasks.models import Task
from tasks.serializer.task_serializer import (
    TaskListSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer
)


class TaskViewset(BaseModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """

    queryset = Task.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    serializer_class = TaskListSerializer

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TaskListSerializer
        if self.action in ['create']:
            return TaskCreateSerializer
        if self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return self.serializer_class

    swagger_auto_schema(
        operation_description=_('List of tasks'),
        responses={
            200: TaskListSerializer,
            400: _('You dont have access to this information')
        }
    )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if isinstance(response, Response) and not response.data:
            return Response(
                {"detail": _("No tienes tareas asignadas.")},
                status=status.HTTP_404_NOT_FOUND
            )
        return response
    swagger_auto_schema(
        operation_description=_(' list of a especific task'),
        responses={
            200: TaskListSerializer,
            400: _('You dont have access to this information'),
            403: _('The task you are trying to access is not active or already deleted')
        }
    )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if not instance.is_active:
                return Response(
                    {"detail": _(
                        "La tarea solicitada está desactivada o fue eliminada.")},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except NotFound:
            raise NotFound({"detail": _("Tarea no encontrada.")})

    swagger_auto_schema(
        operation_description=_('Create a new task'),
        responses={
            201: _('Task created successfuly'),
            403: _(' You dont have access to this information'),
            400: _('Invalid data')

        }
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Task created successfuly', 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response({'message': 'task could not be created', 'error': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    swagger_auto_schema(
        operation_description=_('Update a especific task'),
        responses={
            200: TaskListSerializer,
            400: _('Invalid data'),
            403: _('You dont have access to this information'),
            404: _('Task not found')
        }
    )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not instance.is_active:
            return Response({'error': _('The Task do you want to update is not active or already deleted')},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Task successfuly updated', 'data': serializer.data},
                            status=status.HTTP_200_OK)

    swagger_auto_schema(
        operation_description=_(
            ' Delete a task or deactivating a task and change status to archived'),
        responses={
            200: TaskListSerializer,
            400: _('Invalid data'),
            403: _('You dont have access to this information'),
            404: _('Task not found')
        }
    )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.is_active:
                instacnce.is_active = False
                instance.status = 'archived'
                instance.save()
                return Response({'message': 'Task deactivaded and archived successfuly'},
                                status=status.HTTP_200_OK)
        except:
            return Response({"detail": _("Tarea no encontrada.")}, status=status.HTTP_404_NOT_FOUND)
