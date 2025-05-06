from rest_framework import serializers
from .models import ComplianceProjection, EmissionFactor
from facilities.models import Facility, FacilityEmission

class FacilitySerializer(serializers.ModelSerializer):
    """
    Serializer for the Facility model.
    
    This is a starter implementation. Candidates should extend this serializer
    with additional fields and methods as needed.
    """
    class Meta:
        model = Facility
        fields = '__all__'


class FacilityEmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for the FacilityEmission model.
    
    This is a starter implementation. Candidates should extend this serializer
    with additional fields and methods as needed.
    """
    class Meta:
        model = FacilityEmission
        fields = '__all__'


class ComplianceProjectionSerializer(serializers.ModelSerializer):
    """
    Serializer for the ComplianceProjection model.
    
    This is a starter implementation. Candidates should extend this serializer
    with additional fields and methods as needed.
    """
    class Meta:
        model = ComplianceProjection
        fields = '__all__'


class EmissionFactorSerializer(serializers.ModelSerializer):
    """
    Serializer for the EmissionFactor model.
    
    This is a starter implementation. Candidates should extend this serializer
    with additional fields and methods as needed.
    """
    class Meta:
        model = EmissionFactor
        fields = '__all__'
