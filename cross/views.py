from django.shortcuts import render_to_response
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from . import models, serializers
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import numpy as np
import cv2
from django.views.decorators.cache import cache_page
#from django.conf import settings

#CACHE_TTL = getattr(settings, 'CACHE_TTL')


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

"""
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
"""

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
    
    """
    def get(self, request, *args, **kwargs):
        place_list = models.Place.objects.all()
        context = {}
        context['place_list'] = place_list
        return self.render_to_response(context)
    """

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":            
            title = request.POST.get("title")
            picture = request.FILES.get("picture")
            datetime = request.POST.get("datetime")
            time_str = request.POST.get("time_str")
            detail_title = request.POST.get("detail_title")
            place_id = request.POST.get("place")
            longitude = request.POST.get("longitude")
            latitude = request.POST.get("latitude")

            place = models.Place.objects.get(id=place_id)   
            if not longitude:
                longitude = place.longitude
            if not latitude:
                latitude = place.latitude

            picture = models.CrossPicture(title=title, 
                            picture=picture, 
                            datetime=datetime, 
                            time_str=time_str, 
                            detail_title=detail_title, 
                            place=place, 
                            longitude=longitude, 
                            latitude=latitude)
            picture.save()            
            return HttpResponse("添加成功")
        elif request.method == "GET":
            place_list = models.Place.objects.all()
            context = {}
            context['place_list'] = place_list
            return self.render_to_response(context) 
 

class laboratory(TemplateView):

    template_name = 'laboratory.html'
    """
    def get_context_data(self, **kwargs):
        context = {}
        return self.render_to_response(context)
    """



@csrf_exempt
def similar_pictures(request):
    picture = request.FILES.get("picture")
    count = 0
    num = 20
    threshold = 12
    similar_list = []
    if picture:
        picture_list = models.CrossPicture.objects.all()
        for p in picture_list:
            if p.picture:
                similar = cal_similar(picture, p)
                if similar < threshold:
                    similar_list.append([p, similar])
                    count += 1
                if count >= num: break
    context = {}
    context['similar_list'] = similar_list
    return render_to_response('laboratory.html', {'similar_list': similar_list})


def cal_similar(p1, p2):
    image1 = np.array(Image.open(p1).convert('L'))
    image2 = np.array(Image.open(p2.picture).convert('L'))   
    h1 = p_hash(image1)
    h2 = p_hash(image2)
    return hamming(h1, h2)
        

def p_hash(src):        
    src = cv2.resize(src, (8, 8), cv2.INTER_LINEAR)
    avg = sum([sum(src[i]) for i in range(8)]) / 64
    string = ''
    for i in range(8):
        string += ''.join(map(lambda i: '0' if i < avg else '1', src[i]))    
    result = ''
    for i in range(0, 64, 4):
        result += ''.join('%x' % int(string[i: i + 4], 2))
    return result
        

def hamming(str1, str2):
    if len(str1) != len(str2): return
    count = 0
    for i in range(0, len(str1)):
        if str1[i] != str2[i]:
            count += 1
    return count 


class place_show(TemplateView):
    template_name = 'place_show.html'

    def get(self, request, id, *args, **kwargs):
        place = models.Place.objects.get(id=id)
        context = {}
        context['place'] = place  
        return self.render_to_response(context)


