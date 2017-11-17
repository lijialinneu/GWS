from django.conf.urls import patterns, url
from account import views

 
urlpatterns = patterns('',
    url(r'^$', views.sign_in, name='sign_in'),
    url(r'^sign_up/$',views.sign_up, name='sign_up'),
)
