from django.shortcuts import render_to_response
from django.http.response import HttpResponse
from . import models, serializers
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from PIL import Image

def home(request):
    return render_to_response('homepage.html')

def page_not_found(request):
    return render_to_response('404.html')


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = models.Place.objects.all()
    serializer_class = serializers.PlaceSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        place_name = request.GET.get('name')
        if place_name is not None:
            queryset = models.Place.objects.filter(name__contains=place_name)
        else:
            queryset = models.Place.objects.all()
        serializer = serializers.PlaceSerializer(queryset, many=True)
        return Response(serializer.data)


class CrossPictureViewSet(viewsets.ModelViewSet):
    queryset = models.CrossPicture.objects.all()
    serializer_class = serializers.CrossPictureSerializer
    permission_classes = [permissions.AllowAny]
#     permission_classes = [IsAccountAdminOrReadOnly]



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

