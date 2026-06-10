from django.db import models
from django.conf import settings
from django.utils.timezone import now


class AdminLog(models.Model):
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='admin_logs'
    )
    action = models.CharField(max_length=100)
    entity = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(default=now)
    detail = models.TextField(blank=True)

    class Meta:
        app_label = 'mundial'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.admin} — {self.action} — {self.entity} — {self.timestamp:%Y-%m-%d %H:%M}'
