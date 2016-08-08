from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from . import models
from rest_framework.response import Response
from . import serializers
from rest_framework import permissions
from django.http.response import HttpResponse
from rest_framework import status


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = models.Place.objects.all()
    serializer_class = serializers.PlaceSerializer
    permission_classes = [permissions.AllowAny]


class CrossPictureViewSet(viewsets.ModelViewSet):
    queryset = models.CrossPicture.objects.all()
    serializer_class = serializers.CrossPictureSerializer
    permission_classes = [permissions.AllowAny]
#     permission_classes = [IsAccountAdminOrReadOnly]


def test(request):
    pass
    return HttpResponse("OK")
