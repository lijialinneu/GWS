from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views

router = DefaultRouter()
router.register(r'place', views.PlaceViewSet)
router.register(r'picture', views.CrossPictureViewSet)
router.register(r'place/(?P<name>.+)/$', views.PlaceViewSet)

urlpatterns = router.urls
