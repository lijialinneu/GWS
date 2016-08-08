# -*- coding: utf-8 -*-
from rest_framework import serializers
from . import models
from rest_framework.exceptions import APIException


class CrossPictureSerializer(serializers.ModelSerializer):
    #     place = PlaceSerializer(read_only=True)

    class Meta:
        model = models.CrossPicture


class PlaceSerializer(serializers.ModelSerializer):
    cross_pictures = CrossPictureSerializer(many=True, read_only=True)

    class Meta:
        model = models.Place
#         fields = ('pk', 'name','cross_pictures')
        read_only_fields = ('cross_pictures',)

    def create(self, validated_data, *args, **kwargs):
        place_qs = self.Meta.model.objects.filter(city=validated_data['city'],
                                                  name=validated_data['name']
                                                  )
        if place_qs:
            raise APIException("city: {}中已经有名为{}的地点,请重新添加".format(
                validated_data['name'], validated_data['city']))

        return super(PlaceSerializer, self).create(validated_data, *args, **kwargs)
