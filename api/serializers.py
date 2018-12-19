from meteorite_landings.models import CountryArea, DevStatus, MeteoriteClass, MeteoriteLanding,\
    Location, Planet, Region, SubRegion, IntermediateRegion
from rest_framework import response, serializers, status

class PlanetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Planet
        fields = ('planet_id', 'planet_name', 'unsd_name')

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ('region_id', 'region_name', 'planet_id')

class SubRegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubRegion
        fields = ('sub_region_id', 'sub_region_name', 'region_id')

class IntermediateRegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = IntermediateRegion
        fields = ('intermediate_region_id', 'intermediate_region_name', 'sub_region_id')

class LocationSerializer(serializers.ModelSerializer):
    planet = PlanetSerializer(many=False, read_only=True)
    region = RegionSerializer(many=False, read_only=True)
    sub_region = SubRegionSerializer(many=False, read_only=True)
    intermediate_region = IntermediateRegionSerializer(many=False, read_only=True)

    class Meta:
        model = Location
        fields = ('location_id', 'planet', 'region', 'sub_region', 'intermediate_region')

class DevStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = DevStatus
        fields = ('dev_status_id', 'dev_status_name')

class CountryAreaSerializer(serializers.ModelSerializer):
    dev_status = DevStatusSerializer(many=False, read_only=True)
    location = LocationSerializer(many=False, read_only=True)

    class Meta:
        model = CountryArea
        fields = (
            'country_area_id',
            'country_area_name',
            'm49_code',
            'iso_alpha3_code',
            'dev_status',
            'location'
        )

class MeteoriteLandingSerializer(serializers.ModelSerializer):
    country_area_id = serializers.ReadOnlyField(source='country_area.country_area_id')
    meteorite_class_id = serializers.ReadOnlyField(source='meteorite_class.meteorite_class_id')

    class Meta:
        model = MeteoriteLanding
        fields = (
            'meteorite_landing_id',
            'country_area_id',
            'meteorite_class_id',
            'count',
            'average_mass',
            'max_mass',
            'min_mass',
        )

class MeteoriteClassSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        allow_blank=False,
        max_length=255
    )
    definition = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = MeteoriteLanding
        fields = (
            'meteorite_class_id',
            'code',
            'definition',
            'description'
        )

    def create(self, validated_data):
        meteorite_class = MeteoriteClass.objects.create(**validated_data)
        return meteorite_class

    def update(self, instance, validated_data):
        meteorite_class_id = instance.meteorite_class_id

        instance.code = validated_data.get(
            'code',
            instance.code
        )

        instance.definition = validated_data.get(
            'definition',
            instance.definition
        )

        instance.description = validated_data.get(
            'description',
            instance.description
        )

        instance.save()

        return instance
