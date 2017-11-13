from django.shortcuts import render_to_response
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView, View
from . import models, serializers
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from PIL import Image
import random
import numpy as np

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

    def get(self, request, *args, **kwargs):        
        name = request.GET.get("name")
        if not name:
            place_list = models.Place.objects.all()
        else:
            place_list = models.Place.objects.filter(name__contains=name)
        context = {}
        context['place_list'] = place_list
        return self.render_to_response(context)


class picture_list(TemplateView):
    template_name = 'picture_list.html'

    def get_context_data(self,  **kwargs):        
        picture_list = models.CrossPicture.objects.all()
        context = {}
        context['picture_list'] = picture_list    
        return context


class add_place(TemplateView):
    template_name = 'add_place.html'

    def get(self, request, *args, **kwargs):
        name = request.GET.get("name")
        lng = request.GET.get("longitude")
        lat = request.GET.get("latitude")    
        place = None
        if name and lng and lat:            
            place = models.Place.objects.create(name=name, longitude=lng, latitude=lat)        
        
        context = {}
        context['result'] = place
        return self.render_to_response(context)


class add_picture(TemplateView):
    template_name = 'add_picture.html'
    
    def get(self, request, *args, **kwargs):
        title = request.GET.get("title")
        picture = request.GET.get("picture")
        datetime = request.GET.get("datetime")
        time_str = request.GET.get("time_str")
        detail_title = request.GET.get("detail_title")
        place = request.GET.get("place")
        longitude = request.GET.get("longitude")
        latitude = request.GET.get("latitude")
        
        if title and picture and datetime and time_str and place: 
            picture = models.CrossPicture.objects.create(
                title=title, picture=picture, datetime=datetime, 
                time_str=time_str, detail_title=detail_title,
                place=place, longitude=longitude, latitude=latitude)
       
        context = {}
        context['result'] = picture            
        return self.render_to_response(context)
    

    """
    def get_context_data(self, **kwargs):        
        context = {}
        context['result'] = '200'
        return context
    """


class similar_pictures(TemplateView):
    template_name = 'similar_pictures.html'
    
    def get(self, request, *args, **kwargs):
        input_picture = request.GET.get("picture")
        similar_list = []
        if input_picture:      
            picture_list = models.CrossPicture.objects.all()            
            num = 0
            th = 30 # threshold
            for picture in picture_list:
                if num >= 20:
                    break
                num += 1
                similar = self.similar(input_picture, picture)
                if similar < th :
                    similar_list.append([picture, similar])
        context = {}
        context['similar_list'] = similar_list
        return self.render_to_response(context)

    def similar(self, input_picture, picture):
        return random.uniform(0, 100)
        '''
        image1 = np.array(Image.open(input_picture).convert('L'))
        image2 = np.array(Image.open(picture).convert('L'))
        h1 = self.p_hash(mat1)
        h2 = self.p_hash(mat2)
        return self.hamming(h1, h2)
        '''

    def p_hash(self, src):        
        src.thumbnail((8,8), Image.ANTIALIAS)
        avg = sum([sum(src[i]) for i in range(8)]) / 64
        string = ''
        for i in range(8):
            string += ''.join(map(lambda i: '0' if i < avg else '1', src[i]))    
        result = ''
        for i in range(0, 64, 4):
            result += ''.join('%x' % int(string[i: i + 4], 2))
        return result
        
    
