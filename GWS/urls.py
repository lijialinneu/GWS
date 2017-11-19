"""GWS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.views.decorators.cache import cache_page
import cross
import account

CACHE_TTL = getattr(settings, 'CACHE_TTL')

urlpatterns = ([
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cross/', include('cross.urls')),
    # url(r'^compress/', cross.views.compressImage),
    url(r'^place_list/$', cache_page(CACHE_TTL)(cross.views.place_list.as_view()), name="place_list"),
    url(r'^picture_list/$', cache_page(CACHE_TTL)(cross.views.picture_list.as_view()), name="picture_list"),
    url(r'^add_place/$', cross.views.add_place.as_view(), name="add_place"),
    url(r'^add_picture/$', cache_page(CACHE_TTL)(cross.views.add_picture.as_view()), name="add_picture"),
    url(r'^laboratory/$', cross.views.laboratory.as_view(), name="laboratory"),
    url(r'^similar_pictures/$', cross.views.similar_pictures),
    url(r'^place_show/(?P<id>\d+)/$', cross.views.place_show.as_view(), name="place_show"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^$',cache_page(CACHE_TTL)(cross.views.home), name="home"),
    url('^account/', include('account.urls', namespace='account'))
]) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = cross.views.page_not_found

