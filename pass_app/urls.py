from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BarcodeViewSet,
    DownloadFullPass,
    DownloadPassJSON,
    FieldViewSet,
    ImageViewSet,
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
router.register(r'images', ImageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('download/<int:pk>/', DownloadPassJSON.as_view(), name='download_pass'),
    path('downloadzip/<int:pk>/', DownloadFullPass.as_view(), name='download_zip')
]
