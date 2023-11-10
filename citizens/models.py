from django.db import models

# Create your models here.
class Image(models.Model):
    photo = models.ImageField(upload_to="images")


class Notification(models.Model):
    image = models.ImageField(upload_to="notifications",default="")
    case_name = models.CharField(max_length=255,default="")
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    closestPoliceStation = models.CharField(max_length=255)
    govid = models.CharField(max_length=255,default="")
    rootPoliceStation = models.CharField(max_length=255)
    
