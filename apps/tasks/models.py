from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.base.models import AuditableMixins
from users.models import User


# Create your models here.

class Task(AuditableMixins, models.Model):
    """Task Model"""

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('archived', 'Archived')
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks', verbose_name=_('owner'))
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    status = models.CharField(
        _('status'), max_length=20, choices=STATUS_CHOICES, default='pendiente')
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    def __str__(self):
        return self.title
