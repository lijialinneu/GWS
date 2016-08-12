# -*- coding: utf-8 -*-
from django.db import models
import json
import urllib
import requests
from pip._vendor.requests.exceptions import HTTPError
from difflib import Match


class Place(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    altitude = models.FloatField(default=0.0)
    city = models.ForeignKey("City", blank=True, null=True)

    def __str__(self):
        if not self.city:
            print('look up')
            self.look_up_city()
            self.save()
        if not self.city:
            city = City.objects.get_city('No City Match', city_code=000000)
            self.city = city
            self.save()
        return '的'.join([str(self.city), self.name])

    @property
    def cross_pictures(self):
        return self.crosspicture_set.all()

    def look_up_city(self):
        url = ('http://api.map.baidu.com/geocoder/v2/?'
               'ak=IiiPZfBRZ8PIWlMPF2tc4vnWZtxSvWIQ'
               '&coordtype=wgs84ll'
               '&callback=renderReverse&location={},{}'
               '&output=json'
               '&pois=0').format(self.latitude, self.longitude)
        r = requests.request(
            method="get",
            url=url,
        )
        for i in range(3):
            try:
                r.raise_for_status()
                text = r.text
                break
            except HTTPError as e:
                text = None
        if text:
            try:
                result_dict = json.loads(text[29:-1])
                address_component = result_dict['result']['addressComponent']
                print(address_component)
                city_name = address_component['city']
                province_name = address_component['province']
                country_name = address_component['country']
                city_code = result_dict['result']['cityCode']
                if not city_name:
                    city_name = "NONE_NAME_CITY: {}".format(city_code)
                city = City.objects.get_city(
                    city_name, city_code, province_name, country_name)
                self.city = city

            except:
                pass
        return dict


class CrossPicture(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='cross_picture')
    datetime = models.DateTimeField()
    time_str = models.CharField(max_length=100)
    detail_url = models.CharField(max_length=255, blank=True, null=True)
    detail_title = models.CharField(max_length=100, blank=True, null=True)
    like_count = models.IntegerField(default=0, null=True)
    place = models.ForeignKey(Place)  # ,related_name='place_crosspictures')
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True, default=0.0)

    class Meta:
        ordering = ('datetime',)


class CityManager(models.Manager):

    def get_city(self, city_name, city_code, province_name=None, country_name=None):
        city_qs = self.filter(code=city_code)
        if city_qs:
            city = city_qs[0]
        else:
            if province_name:
                province = Province.objects.get_province(
                    province_name, country_name)
            else:
                province = None
            city = self.create(
                name=city_name, code=city_code, province=province)
        return city


class ProvinceManager(models.Manager):

    def get_province(self, province_name, country_name=None):
        province_qs = self.filter(name=province_name)
        if province_qs:
            province = province_qs[0]
        else:
            if country_name:
                country = Country.objects.get_country(country_name)
            else:
                country = None
            province = self.create(name=province_name, country=country)
        return province


class CountryManager(models.Manager):

    def get_country(self, country_name):
        country_qs = self.filter(name=country_name)
        if country_qs:
            country = country_qs[0]
        else:
            country = self.create(name=country_name)
        return country


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, null=True)

    objects = CountryManager()

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, null=True)
    country = models.ForeignKey(Country, null=True)

    objects = ProvinceManager()

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, null=True)
    province = models.ForeignKey(Province, null=True)

    objects = CityManager()

    def __str__(self):
        return self.name
