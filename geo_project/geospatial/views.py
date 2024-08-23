from typing import List, Dict, Any
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.gis.geos import LineString as GEOSLineString, Point as GEOSPoint
from .models import Point, LineString, Polygon
from .serializers import PointSerializer, LineStringSerializer, PolygonSerializer
from rest_framework_gis.fields import GeometryField


class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract coordinates from the incoming Point
        incoming_location = serializer.validated_data['location']
        incoming_coords = list(incoming_location.coords)

        # Check if a Point with these coordinates already exists
        if self.point_exists(incoming_coords):
            return Response(
                {"detail": "Point with these coordinates already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Proceed with creation if no duplicates
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def point_exists(self, coords: List[float]) -> bool:
        """Check if a Point with the given coordinates already exists in the database."""
        for point in Point.objects.all():
            if list(point.location.coords) == coords:
                return True
        return False

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Point was successfully deleted."},
            status=status.HTTP_204_NO_CONTENT
        )


class LineStringViewSet(viewsets.ModelViewSet):
    queryset = LineString.objects.all()
    serializer_class = LineStringSerializer

    @action(detail=False, methods=['post'])
    def join_lines(self, request: Request) -> Response:
        line_ids = request.data.get('lines', [])
        lines = LineString.objects.filter(id__in=line_ids)

        if not lines:
            return Response(
                {'error': 'No lines provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Initialize a list to hold all coordinates
        coords = []

        # Add coordinates of each line to the list
        for line in lines:
            line_coords = list(line.path.coords)

            # Avoid duplicating the start of the new line if it's the same as the end of the previous line
            if coords and coords[-1] == line_coords[0]:
                coords.extend(line_coords[1:])  # Skip the first point if it's a duplicate
            else:
                coords.extend(line_coords)

        # Create a new LineString with concatenated coordinates
        joined_line = GEOSLineString(coords)

        # Convert to GeoJSON
        geojson = GeometryField().to_representation(joined_line)

        return Response({"type": "Feature", "geometry": geojson})

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract coordinates from the incoming LineString
        incoming_path = serializer.validated_data['path']
        incoming_coords = list(incoming_path.coords)

        # Check for duplicates
        if self.line_exists(incoming_coords):
            return Response(
                {"detail": "LineString with these coordinates already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Proceed with creation if no duplicates
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def line_exists(self, coords: List[float]) -> bool:
        """Check if a LineString with the given coordinates already exists in the database."""
        for line in LineString.objects.all():
            if list(line.path.coords) == coords:
                return True
        return False

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'detail': 'Data was deleted'},
            status=status.HTTP_204_NO_CONTENT
        )


class PolygonViewSet(viewsets.ModelViewSet):
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer

    @action(detail=True, methods=['post'])
    def intersection(self, request: Request, pk: int = None) -> Response:
        polygon = self.get_object()
        print(f"Polygon boundary: {polygon.boundary}")

        point_ids = request.data.get('points', [])
        points = Point.objects.filter(id__in=point_ids)

        intersects = []
        for point in points:
            # Ensure the SRID matches
            point_geom = GEOSPoint(point.location.x, point.location.y, srid=4326)
            if polygon.boundary.contains(point_geom):
                intersects.append(point)
            print(f"Point location: {point.location}, is within: {polygon.boundary.contains(point_geom)}")

        serializer = PointSerializer(intersects, many=True)
        return Response(serializer.data)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Polygon was successfully deleted."},
            status=status.HTTP_204_NO_CONTENT
        )
