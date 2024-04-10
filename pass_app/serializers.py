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
                  'secondaryFields', 'backFields', 'auxiliaryFields']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = instance.get_dict()
        return data


class PassSerializer(serializers.ModelSerializer):
    pass_information = PassInformationSerializer(many=True)
    barcode = BarcodeSerializer()
    locations = LocationSerializer()

    class Meta:
        model = Pass
        fields = ['formatVersion', 'description', 'passTypeIdentifier', 'serialNumber',
                  'teamIdentifier', 'organizationName', 'webServiceURL', 'authenticationToken',
                  'suppressStripShine', 'relevantDate', 'logoText', 'foregroundColor',
                  'backgroundColor', 'labelColor', 'expirationDate', 'pass_information', 'barcode', 'locations']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data = instance.get_full_dict()

        return data
