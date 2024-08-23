from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PointViewSet, LineStringViewSet, PolygonViewSet

router = DefaultRouter()
router.register(r'points', PointViewSet)
router.register(r'linestrings', LineStringViewSet)
router.register(r'polygons', PolygonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
