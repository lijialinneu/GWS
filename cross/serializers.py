# -*- coding: utf-8 -*-
from rest_framework import serializers
from . import models
from rest_framework.exceptions import APIException


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = ('pk',)

class CrossPictureSerializer(serializers.ModelSerializer):
    #     place = PlaceSerializer(read_only=True)

    class Meta:
        model = models.CrossPicture
        fields = ('pk', 'title', 'picture','datetime', 'time_str','detail_title','place', 'longitude', 'latitude')

class PlaceSerializer(serializers.ModelSerializer):
    cross_pictures = CrossPictureSerializer(many=True, read_only=True)
    city = CitySerializer(read_only=True)
    class Meta:
        model = models.Place
        fields = ('pk', 'name', 'longitude', 'latitude', 'city', 'cross_pictures')
        read_only_fields = ('cross_pictures',)

    def create(self, validated_data, *args, **kwargs):
        city = self.Meta.model.look_up_city(latitude=validated_data['latitude'],
                                            longitude=validated_data['longitude'] ,
                                            )
        validated_data['city'] = city
        place_qs = self.Meta.model.objects.filter(city=validated_data['city'],
                                                  name=validated_data['name']
                                                  )
        if place_qs:
            raise APIException('city: "{}"中已经有名为"{}"的地点,请重新添加'.format(
                validated_data['city'], validated_data['name']))

        return super(PlaceSerializer, self).create(validated_data, *args, **kwargs)
