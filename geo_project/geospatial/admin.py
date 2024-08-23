from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import Point, LineString, Polygon

class PointAdmin(GISModelAdmin):
    list_display = ('id', 'location')  # Display the ID and location fields in the list view
    search_fields = ('id',)            # Add search functionality for IDs
    list_filter = ('location',)        # Add filter functionality based on location

class LineStringAdmin(GISModelAdmin):
    list_display = ('id', 'path')      # Display the ID and path fields in the list view
    search_fields = ('id',)            # Add search functionality for IDs
    list_filter = ('path',)            # Add filter functionality based on path

class PolygonAdmin(GISModelAdmin):
    list_display = ('id', 'boundary')  # Display the ID and boundary fields in the list view
    search_fields = ('id',)            # Add search functionality for IDs
    list_filter = ('boundary',)        # Add filter functionality based on boundary

# Register the models with their respective admin classes
admin.site.register(Point, PointAdmin)
admin.site.register(LineString, LineStringAdmin)
admin.site.register(Polygon, PolygonAdmin)
