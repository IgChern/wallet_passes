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
    headerFields = FieldSerializer(many=True, required=False)
    primaryFields = FieldSerializer(many=True, required=False)
    secondaryFields = FieldSerializer(many=True, required=False)
    backFields = FieldSerializer(many=True, required=False)
    auxiliaryFields = FieldSerializer(many=True, required=False)

    class Meta:
        model = PassInformation
        fields = ['headerFields', 'primaryFields',
                  'secondaryFields', 'backFields', 'auxiliaryFields', 'json_name']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = {key: value for key, value in data.items() if value}
        return data


class PassSerializer(serializers.ModelSerializer):
    pass_information = PassInformationSerializer(many=True)
    barcode = BarcodeSerializer()
    location = LocationSerializer()

    class Meta:
        model = Pass
        fields = ['formatVersion', 'description', 'passTypeIdentifier', 'serialNumber',
                  'teamIdentifier', 'organizationName', 'webServiceURL', 'authenticationToken',
                  'suppressStripShine', 'relevantDate', 'logoText', 'foregroundColor',
                  'backgroundColor', 'labelColor', 'pass_information', 'barcode', 'location']

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
