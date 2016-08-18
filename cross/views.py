from django.shortcuts import render_to_response
from django.http.response import HttpResponse
from . import models, serializers
from rest_framework import viewsets, permissions


def home(request):
    return render_to_response('homepage.html')


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
