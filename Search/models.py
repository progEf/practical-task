from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(null=False, max_length=255)
    subject = models.CharField(null=False, max_length=255)
    lat = models.FloatField(null=False)
    lon = models.FloatField(null=False)
# for i in add_City():                                                                                      '])
#...     City.objects.create(name=i['name'], subject=i['subject'], lat=i['coords']['lat'], lon=i['coords']['lon'])
#