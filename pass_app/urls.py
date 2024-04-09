from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BarcodeViewSet,
    FieldViewSet,
    LocationViewSet,
    PassInformationViewSet,
    PassViewSet,
)

router = DefaultRouter()
router.register(r'passes', PassViewSet)
router.register(r'passinformations', PassInformationViewSet)
router.register(r'fields', FieldViewSet)
router.register(r'barcodes', BarcodeViewSet)
router.register(r'locations', LocationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
