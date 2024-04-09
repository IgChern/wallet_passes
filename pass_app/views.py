from rest_framework import viewsets

from .models import Barcode, Field, Location, Pass, PassInformation
from .serializers import (
    BarcodeSerializer,
    FieldSerializer,
    LocationSerializer,
    PassInformationSerializer,
    PassSerializer,
)


class PassViewSet(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer


class PassInformationViewSet(viewsets.ModelViewSet):
    queryset = PassInformation.objects.all()
    serializer_class = PassInformationSerializer


class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer


class BarcodeViewSet(viewsets.ModelViewSet):
    queryset = Barcode.objects.all()
    serializer_class = BarcodeSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
