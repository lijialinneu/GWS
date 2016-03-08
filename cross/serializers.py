from rest_framework import serializers
from . import models





        
class CrossPictureSerializer(serializers.ModelSerializer):
#     place = PlaceSerializer(read_only=True)
    class Meta:
        model = models.CrossPicture

class PlaceSerializer(serializers.ModelSerializer):
    cross_pictures = CrossPictureSerializer(many = True,read_only = True)
    class Meta:
        model = models.Place
#         fields = ('pk', 'name','cross_pictures')
        read_only_fields = ('cross_pictures')
        