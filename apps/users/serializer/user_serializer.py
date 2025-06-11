from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from apps.base.serializer import AuditableSerializerMixin
from apps.users.models import User
from apps.users.validators import validate_email_address, validate_password_strength


class UserListSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'created_by',
                  'created_date', 'updated_by', 'updated_date', 'is_active']
        read_only_fields = ['__all__']


class UserCreateSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'is_active',
                  'created_date', 'created_by', 'updated_date', 'updated_by']
        read_only_fields = ['created_date',
                            'created_by', 'updated_date', 'updated_by']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': [validate_email_address]}
        }

    def validate(self, data):
        if 'password' in data:
            validate_password_strength(
                data['password'], data.get('username', ''))
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserUpdateSerializer(UserCreateSerializer):
    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)

    class Meta(UserCreateSerializer.Meta):
        fields = [
            'first_name',
            'last_name',
            'old_password',
            'new_password',
            'updated_date',
            'updated_by'
        ]
        read_only_fields = ['email', 'is_active', 'updated_date', 'updated_by']

    def validate(self, data):
        if 'new_password' in data:
            if 'old_password' not in data:
                raise serializers.ValidationError(
                    {"old_password": "Debes proporcionar tu contraseña actual."}
                )

            if not check_password(data['old_password'], self.instance.password):
                raise serializers.ValidationError(
                    {"old_password": "Contraseña actual incorrecta."}
                )

            if check_password(data['new_password'], self.instance.password):
                raise serializers.ValidationError(
                    {"new_password": "La nueva contraseña no puede ser igual a la anterior."}
                )

            validate_password_strength(
                data['new_password'], self.instance.username)

        return data

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)

        if 'new_password' in validated_data:
            instance.set_password(validated_data['new_password'])

        instance.save()
        return instance
