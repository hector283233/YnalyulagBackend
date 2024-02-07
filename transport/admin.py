from django.contrib import admin

from .models import (Transport, Locations, Trip, Comments)

admin.site.register(Transport)
admin.site.register(Locations)
admin.site.register(Trip)
admin.site.register(Comments)