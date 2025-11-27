from django.db import models

# Create your models here.

class PageView(models.Model):
    url = models.CharField(max_length=255)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url} - {self.timestamp}"
