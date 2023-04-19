from django.db import models

# Create your models here.
class Foods(models.Model):
    cook_name = models.CharField(max_length=50)
    count = models.IntegerField()
    unit_price = models.IntegerField()