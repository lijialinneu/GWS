from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from . import models
from rest_framework.response import Response
from . import serializers
from rest_framework import permissions

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = models.Place.objects.all()
    serializer_class = serializers.PlaceSerializer
    permission_classes = [permissions.AllowAny]

class CrossPictureViewSet(viewsets.ModelViewSet):
    queryset = models.CrossPicture.objects.all()
    serializer_class = serializers.CrossPictureSerializer
    permission_classes = [permissions.AllowAny]
#     permission_classes = [IsAccountAdminOrReadOnly]