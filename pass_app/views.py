import json

from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

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


class DownloadPassJSON(APIView):
    def get(self, request, pk):
        pass_instance = Pass.objects.get(pk=pk)
        pass_data = pass_instance.get_full_dict()

        pass_json = json.dumps(pass_data, ensure_ascii=False)

        response = HttpResponse(pass_json, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="pass.json"'

        return response
