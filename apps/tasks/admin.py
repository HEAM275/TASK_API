# apps/tasks/admin.py
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from apps.base.utils import get_user_fullname
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'is_active', 'created_date')
    search_fields = ('title', 'description', 'owner__email')
    list_filter = ('status', 'is_active', 'created_date')
    readonly_fields = ('created_date', 'created_by', 'updated_date',
                       'updated_by', 'deleted_date', 'deleted_by')

    fieldsets = (
        (_('Tarea'), {
            'fields': ('title', 'description', 'status', 'is_active')
        }),
        (_('Auditoría'), {
            'fields': (
                'created_date', 'created_by',
                'updated_date', 'updated_by',
                'deleted_date', 'deleted_by'
            )
        }),
        (_('Relaciones'), {
            'fields': ('owner',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Si es una creación
            if request.user.is_authenticated:
                obj.created_by = get_user_fullname(request.user)
                obj.created_date = timezone.now()
        else:  # Si es una actualización
            if request.user.is_authenticated:
                obj.updated_by = get_user_fullname(request.user)
                obj.updated_date = timezone.now()

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if request.user.is_authenticated:
            obj.deleted_by = get_user_fullname(request.user)
            obj.deleted_date = timezone.now()
            obj.is_active = False
            obj.save()
        else:
            obj.is_active = False
            obj.deleted_by = "Anónimo"
            obj.deleted_date = timezone.now()
            obj.save()
