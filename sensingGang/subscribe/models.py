from django.db import models
from datetime import date

# Create your models here.
class Sensors(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class DataEntries(models.Model):
    sensor = models.ForeignKey(Sensors, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    data = models.TextField()
    pub_date = models.DateField()
    
class Entry(models.Model):
    topic = models.CharField(max_length=255)
    data = models.FloatField()
    pub_date = models.DateField()
    
class Entry2(models.Model):
    topic = models.CharField(max_length=255)
    data = models.FloatField()
    pub_date = models.DateTimeField()
    
class Product(models.Model):
    category = models.CharField(max_length=100, null=False, blank=False)
    num_of_products = models.IntegerField()

    def __str__(self):
        return f'{self.category} - {self.num_of_products}'
        
class Subscriptions(models.Model):
    username = models.CharField(max_length=255, null=False, blank=False)
    sensorX = models.BooleanField(default=False)
    sensorY = models.BooleanField(default=False)
    sensorZ = models.BooleanField(default=False)