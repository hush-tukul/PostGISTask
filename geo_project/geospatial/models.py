from django.contrib.gis.db import models

class Point(models.Model):
    location = models.PointField(srid=4326)  # EPSG:4326 is WGS84

    def __str__(self):
        return f"Point({self.location.x}, {self.location.y})"

class LineString(models.Model):
    path = models.LineStringField(srid=4326)

    def __str__(self):
        return f"LineString({self.path})"

class Polygon(models.Model):
    boundary = models.PolygonField(srid=4326)

    def __str__(self):
        return f"Polygon({self.boundary})"
