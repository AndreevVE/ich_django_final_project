from django.db import models
from django.utils.translation import gettext_lazy as _

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class BaseModel(models.Model):
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    is_deleted = models.BooleanField(_('Мягко удалено'), default=False)

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])


