# -*- coding: utf-8 -*-
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    altitude = models.FloatField(default = 0.0)
    
    def __str__(self):
        return self.name
    
    @property
    def cross_pictures(self):
        return self.crosspicture_set.all()


class CrossPicture(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='cross_picture', blank=True)
    datetime = models.DateTimeField()
    time_str = models.CharField(max_length=100)
    detail_url = models.CharField(max_length=255,blank=True,null=True)
    detail_title = models.CharField(max_length=100,blank=True,null=True)
    like_count = models.IntegerField(default = 0)
    place = models.ForeignKey(Place)#,related_name='place_crosspictures')
    longitude = models.FloatField(blank = True,null=True)
    latitude = models.FloatField(blank = True,null=True)
    altitude = models.FloatField(blank = True,null=True,default = 0.0)
    
