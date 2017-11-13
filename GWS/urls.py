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
import cross


urlpatterns = ([
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cross/', include('cross.urls')),
    # url(r'^compress/', cross.views.compressImage),i
    url(r'^place_list/$', cross.views.place_list.as_view()),
    url(r'^picture_list/$', cross.views.picture_list.as_view()),
    url(r'^add_place/$', cross.views.add_place.as_view()),
    url(r'^add_picture/$', cross.views.add_picture.as_view()),
    url(r'^similar_pictures/$', cross.views.similar_pictures.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^$',cross.views.home),
]) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = cross.views.page_not_found

