from rest_framework import serializers

from .models import Barcode, Field, Location, Pass, PassInformation


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['key', 'value', 'label', 'change_message', 'text_alignment']


class BarcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barcode
        fields = ['message', 'format', 'message_encoding', 'alt_text']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude', 'altitude']


class PassInformationSerializer(serializers.ModelSerializer):
    header_fields = FieldSerializer(many=True, required=False)
    primary_fields = FieldSerializer(many=True, required=False)
    secondary_fields = FieldSerializer(many=True, required=False)
    back_fields = FieldSerializer(many=True, required=False)
    auxiliary_fields = FieldSerializer(many=True, required=False)

    class Meta:
        model = PassInformation
        fields = ['header_fields', 'primary_fields',
                  'secondary_fields', 'back_fields', 'auxiliary_fields']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value}


class PassSerializer(serializers.ModelSerializer):
    passInformation = PassInformationSerializer()
    barcode = BarcodeSerializer()
    location = LocationSerializer()

    class Meta:
        model = Pass
        fields = ['formatVersion', 'description', 'passTypeIdentifier', 'serialNumber',
                  'teamIdentifier', 'organizationName', 'webServiceURL', 'authenticationToken',
                  'suppressStripShine', 'relevantDate', 'logoText', 'foregroundColor',
                  'backgroundColor', 'labelColor', 'passInformation', 'barcode', 'location']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        optional_fields = ['webServiceURL', 'authenticationToken', 'suppressStripShine',
                           'relevantDate', 'logoText', 'foregroundColor', 'backgroundColor', 'labelColor']
        for field in optional_fields:
            if getattr(instance, field, None) is not None:
                data[field] = getattr(instance, field)
            else:
                data.pop(field, None)
        return data
