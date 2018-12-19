import django_filters
from meteorite_landings.models import CountryArea, MeteoriteClass, IntermediateRegion, SubRegion, Region

class MeteoriteClassFilter(django_filters.FilterSet):
    meteorite_class = django_filters.CharFilter(
        field_name = 'code',
        label = 'Meteorite Class Code',
        lookup_expr = 'icontains'
    )

    definition = django_filters.CharFilter(
        field_name = 'definition',
        label = 'Definition',
        lookup_expr = 'icontains'
    )

    description = django_filters.CharFilter(
        field_name = 'description',
        label = 'Description',
        lookup_expr = 'icontains'
    )

    region = django_filters.ModelChoiceFilter(
        field_name = 'country_area__location__region__region_name',
        label = 'Region',
        queryset = Region.objects.all().order_by('region_name'),
        lookup_expr='exact'
    )

    sub_region = django_filters.ModelChoiceFilter(
        field_name = 'country_area__location__sub_region__sub_region_name',
        label = 'Sub-Region',
        queryset = SubRegion.objects.all().order_by('sub_region_name'),
        lookup_expr='exact'
    )

    intermediate_region = django_filters.ModelChoiceFilter(
        field_name = 'country_area__location__intermediate_region__intermediate_region_name',
        label = 'Intermediate Region',
        queryset = IntermediateRegion.objects.all().order_by('intermediate_region_name'),
        lookup_expr='exact'
    )

    country_area = django_filters.ModelChoiceFilter(
        field_name = 'country_area',
        label = 'Country/Area',
        queryset = CountryArea.objects.all().order_by('country_area_name'),
        lookup_expr = 'exact'
    )

    class Meta:
        model = MeteoriteClass
        fields = []
