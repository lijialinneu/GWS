from django.conf.urls import patterns, url
from account import views

 
urlpatterns = patterns('',
    url(r'^$', views.register, name='home'),
    url(r'^register/$',views.register,name = 'register'),
)
