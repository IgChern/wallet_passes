import hashlib
import json
import os
import zipfile
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView

from .models import Barcode, Field, Images, Location, Pass, PassInformation
from .serializers import (
    BarcodeSerializer,
    FieldSerializer,
    ImagesSerializer,
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

        pass_json = json.dumps(pass_data, ensure_ascii=False, indent=4)

        response = HttpResponse(pass_json, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="pass.json"'

        return response


class DownloadFullPass(APIView):

    def get_manifest(self, pass_data, buffer):
        hashes = {}

        with zipfile.ZipFile(buffer, 'r') as zipf:
            for filename in zipf.namelist():
                with zipf.open(filename, 'r') as file:
                    file_content = file.read()
                    hashes[filename] = hashlib.sha1(file_content).hexdigest()

        return json.dumps(hashes, indent=4)

    def get(self, request, pk):
        pass_instance = get_object_or_404(Pass, pk=pk)
        pass_data = pass_instance.get_full_dict()

        buffer = BytesIO()

        with zipfile.ZipFile(buffer, 'w') as zipf:
            json_data = json.dumps(pass_data, ensure_ascii=False, indent=4)
            zipf.writestr('pass.json', json_data)

            for image in pass_instance.files.all():
                image_path = image.imagefile.path
                relative_path = os.path.basename(image_path)
                zipf.write(image_path, relative_path)

        manifestjson = self.get_manifest(pass_data, buffer)

        buffer.seek(0)

        with zipfile.ZipFile(buffer, 'a') as zipf:
            zipf.writestr('manifest.json', manifestjson)

        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{pass_instance.json_name}.zip"'
        return response


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
