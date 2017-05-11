from django.shortcuts import render_to_response
from django.http.response import HttpResponse
from . import models, serializers
from rest_framework import viewsets, permissions
from PIL import Image

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


def compressImage(request):
    picture_list = models.CrossPicture.objects.all()
    for cp in picture_list:
        image = Image.open(cp.picture)
        width = image.width
        height = image.height
        rate = 1.0
        if width >= 2000 or height >= 2000:
            rate = 0.3
        elif width >= 1000 or height >= 1000:
            rate = 0.5
        elif width >= 500 or height >= 500:
            rate = 0.9
        width = int(width * rate)
        height = int(height * rate)
        image.thumbnail((width, height), Image.ANTIALIAS)
        image.save('media/' + str(cp.picture), 'JPEG')
        cp.save()
    return HttpResponse('compress finish')

