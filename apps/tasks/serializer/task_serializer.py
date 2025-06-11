from rest_framework import serializers
from apps.base.serializer import AuditableSerializerMixin
from apps.tasks.models import Task


class TaskListSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'is_active',
            'created_date', 'created_by',
            'updated_date', 'updated_by',
            'deleted_date', 'deleted_by'
        ]
        read_only_fields = ['__all__']


class TaskCreateSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Task
        field = [
            'title', 'description', 'status', 'is_active',
            'created_date', 'created_by',
            'updated_date', 'updated_by',
            'deleted_date', 'deleted_by'
        ]
        read_only_fields = [
            'created_date', 'created_by',
            'updated_date', 'updated_by',
            'deleted_date', 'deleted_by'
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "El título no puede estar vacío.")
        return value

    def validate_description(self, value):
        if value is not None and not value.strip():
            raise serializers.ValidationError(
                "La descripción no puede estar vacía.")
        return value


class TaskUpdateSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'status', 'is_active',
            'updated_date', 'updated_by'
        ]
        read_only_fields = [
            'updated_date', 'updated_by'
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "El título no puede estar vacío.")
        return value

    def validate_description(self, value):
        if value is not None and not value.strip():
            raise serializers.ValidationError(
                "La descripción no puede estar vacía.")
        return value
