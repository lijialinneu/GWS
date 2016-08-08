from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Place)
admin.site.register(models.CrossPicture)
admin.site.register(models.City)
admin.site.register(models.Country)
admin.site.register(models.Province)

