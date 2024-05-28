from django.db import models

# Create your models here.
class Address(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}: {self.address}"