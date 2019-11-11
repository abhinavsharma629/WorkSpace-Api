from django.db import models
from django.contrib.auth.models import User
from .genderChoices import GENDER_CHOICES
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.gis.db import models
from django_earthdistance.models import EarthDistanceQuerySet
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.geos import GEOSGeometry

class Photos(models.Model):
    userId=models.OneToOneField(User, on_delete=models.CASCADE, db_column="username")
    photo=models.FileField(upload_to='uploaded_pictures')


class UserDetails(models.Model):
    userId=models.ForeignKey(User, on_delete=models.CASCADE, db_column="username")
    address=models.CharField(max_length=100, null=False, blank=False)
    address1=models.CharField(max_length=100, null=True, blank=True)
    phoneNumber=models.CharField(max_length=14, null=True, blank=True)
    occupation=models.CharField(max_length=1000, null=True, blank=True, default=None)
    state=models.CharField(max_length=100, default=None)
    city=models.CharField(max_length=100, default=None)
    country=models.CharField(max_length=100, default=None)
    alternatePhoneNumber=models.CharField(max_length=14, null=True, blank=True)
    profilePhoto=models.FileField(upload_to='profile_pictures', null=True, blank=True)
    coverPhoto=models.FileField(upload_to='cover_pictures', null=True, blank=True)
    dateOfBirth=models.DateField()
    gender=models.CharField(max_length=100)
    photos=models.ManyToManyField(Photos, blank=True)
    current_lat=models.FloatField(null=True, blank=True)
    current_long=models.FloatField(null=True, blank=True)
    lat_long=models.PointField(srid=4326, null=True,blank=True, spatial_index=True, geography=True)

    def __str__(self):
        return self.userId  
