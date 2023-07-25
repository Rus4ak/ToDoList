from django.db import models

# Create your models here.

class task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    mark = models.BooleanField(default=False, blank=True)
