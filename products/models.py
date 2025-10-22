from django.db import models
from django.core.validators import MinValueValidator


class GuineaPig(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )
    image_url = models.URLField()

    def __str__(self):
        return self.name
