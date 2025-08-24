"""
Definition of models.
"""

from django.db import models
from django.utils import timezone

# Create your models here.

class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.email} - {self.code}"
