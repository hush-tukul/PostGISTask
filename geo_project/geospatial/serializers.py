from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Point, LineString, Polygon

class PointSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Point
        geo_field = 'location'
        fields = ('id', 'location')  # Explicitly listing fields to ensure they are included in the response

class LineStringSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = LineString
        geo_field = 'path'
        fields = ('id', 'path')  # Explicitly listing fields to ensure they are included in the response

class PolygonSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Polygon
        geo_field = 'boundary'
        fields = ('id', 'boundary')  # Explicitly listing fields to ensure they are included in the response
