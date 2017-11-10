from django.shortcuts import render_to_response
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
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


class place_list(TemplateView):
    template_name = 'place_list.html'

    def get_context_data(self, **kwargs):
        place_list = models.Place.objects.all()
        context = {}
        context['place_list'] = place_list
        return context


class picture_list(TemplateView):
    template_name = 'picture_list.html'

    def get_context_data(self,  **kwargs):
        picture_list = models.CrossPicture.objects.all()
        context = {}
        context['picture_list'] = picture_list    
        return context


class add_place(TemplateView):
    template_name='add_place.html'

    def get_context_data(self, **kwargs):        
        context = {}
        context['result'] = '200'
        return context


class add_picture(TemplateView):
    template_name='add_picture.html'

    def get_context_data(self, **kwargs):        
        context = {}
        context['result'] = '200'
        return context





