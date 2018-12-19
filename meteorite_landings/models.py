from django.db import models
from django.urls import reverse
from django.db.models import F, Count, Q

# Create your models here.

class Planet(models.Model):
    planet_id = models.AutoField(primary_key=True)
    planet_name = models.CharField(unique=True, max_length=50)
    unsd_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "planet"
        ordering = ["planet_name"]
        verbose_name = "UNSD Global World"
        verbose_name_plural = "UNSD Global Worlds"

    def __str__(self):
        return self.planet_name

class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(unique=True, max_length=100)
    planet = models.ForeignKey("Planet", on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = "region"
        ordering = ["region_name"]
        verbose_name = "UNESCO Region"
        verbose_name_plural = "UNESCO Regions"

    def __str__(self):
        return self.region_name

class SubRegion(models.Model):
    sub_region_id = models.AutoField(primary_key=True)
    sub_region_name = models.CharField(unique=True, max_length=100)
    region = models.ForeignKey("Region", on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = "sub_region"
        ordering = ["sub_region_name"]
        verbose_name = "UNESCO Sub-Region"
        verbose_name_plural = "UNESCO Sub-Regions"

    def __str__(self):
        return self.sub_region_name

class IntermediateRegion(models.Model):
    intermediate_region_id = models.AutoField(primary_key=True)
    intermediate_region_name = models.CharField(unique=True, max_length=100)
    sub_region = models.ForeignKey("SubRegion", on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = "intermediate_region"
        ordering = ["intermediate_region_name"]
        verbose_name = "UNESCO Intermediate Region"
        verbose_name_plural = "UNESCO Intermediate Regions"

    def __str__(self):
        return self.intermediate_region_name

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    planet = models.ForeignKey("Planet", on_delete=models.PROTECT)
    region = models.ForeignKey("Region", on_delete=models.PROTECT)
    sub_region = models.ForeignKey("SubRegion", on_delete=models.PROTECT)
    intermediate_region = models.ForeignKey("IntermediateRegion", on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = "location"
        ordering = ["location_id"]
        verbose_name = "UNESCO Country Location"
        verbose_name_plural = "UNESCO Country Locations"

    def __str__(self):
        return str(self.location_id)

class DevStatus(models.Model):
    dev_status_id = models.AutoField(primary_key=True)
    dev_status_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = "dev_status"
        ordering = ["dev_status_name"]
        verbose_name = "Development Status"
        verbose_name_plural = "Development Statuses"

    def __str__(self):
        return self.dev_status_name

class CountryArea(models.Model):
    country_area_id = models.AutoField(primary_key=True)
    country_area_name = models.CharField(unique=True, max_length=255)
    m49_code = models.SmallIntegerField()
    iso_alpha3_code = models.CharField(max_length=3)
    location = models.ForeignKey("Location", on_delete=models.PROTECT)
    dev_status = models.ForeignKey("DevStatus", on_delete=models.PROTECT, blank=True, null=True)
    meteorite_class = models.ManyToManyField('MeteoriteClass', through="MeteoriteLanding")

    class Meta:
        managed = False
        db_table = "country_area"
        ordering = ["country_area_name"]
        verbose_name = "UNESCO Country/Area"
        verbose_name_plural = "UNESCO Countries/Areas"

    def __str__(self):
        return self.country_area_name

    def get_absolute_url(self):
        return reverse('country_area_detail', kwargs={'pk': self.pk})

    @property
    def meteorite_class_codes(self):
        meteorite_classes = self.meteorite_class.order_by('code')
        codes = {}
        for meteorite_class in meteorite_classes:
            code = meteorite_class.code
            if code is None:
                continue
            code_definition = meteorite_class.definition

            if code not in codes.keys():
                codes[code] = code_definition
        return codes

class MeteoriteClass(models.Model):
    meteorite_class_id = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=255)
    definition = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    country_area = models.ManyToManyField('CountryArea', through="MeteoriteLanding")

    class Meta:
        managed = False
        db_table = "meteorite_class"
        ordering = ["code"]
        verbose_name = "Meteorite Class"
        verbose_name_plural = "Meteorite Classes"

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('meteorite_class_detail', kwargs={'pk': self.pk})

    @property
    def country_area_name(self):
        countries = self.country_area.select_related('location').order_by('country_area_name')
        names = []
        for country in countries:
            name = country.country_area_name
            if name is None:
                continue
            iso_code = country.iso_alpha3_code

            name_and_code = ''.join([name, ' (', iso_code, ')'])
            if name_and_code not in names:
                names.append(name_and_code)
        return ', '.join(names)

    @property
    def region_names(self):
        regions = self.country_area.select_related('location').values(name=F('location__region__region_name'))
        names = []
        for region in regions:
            name = region['name']
            if name is None:
                continue
            if name not in names:
                names.append(name)
        return ', '.join(names)

    @property
    def sub_region_names(self):
        sub_regions = self.country_area.select_related('location').values(name=F('location__sub_region__sub_region_name'))
        names = []
        for sub_region in sub_regions:
            name = sub_region['name']
            if name is None:
                continue
            if name not in names:
                names.append(name)
        return ', '.join(names)

    @property
    def intermediate_region_names(self):
        intermediate_regions = self.country_area.select_related('location').values(name=F('location__intermediate_region__intermediate_region_name'))
        names = []
        for intermediate_region in intermediate_regions:
            name = intermediate_region['name']
            if name is None:
                continue
            if name not in names:
                names.append(name)
        return ', '.join(names)

class MeteoriteLanding(models.Model):
    meteorite_landing_id = models.AutoField(primary_key=True)
    country_area = models.ForeignKey("CountryArea", on_delete=models.CASCADE)
    meteorite_class = models.ForeignKey("MeteoriteClass", on_delete=models.CASCADE)
    meteorite_count = models.IntegerField(blank=True, default=0)
    average_mass = models.FloatField(blank=True, default=0)
    max_mass = models.FloatField(blank=True, default=0)
    min_mass = models.FloatField(blank=True, default=0)

    class Meta:
        managed = False
        db_table = "meteorite_landing"
        ordering = ["country_area", "meteorite_class"]
        verbose_name = "Meteorite Landing"
        verbose_name_plural = "Meteorite Landings"

    def __str__(self):
        return ' '.join([self.country_area.iso_alpha3_code, self.meteorite_class])

    def get_absolute_url(self):
        return reverse('meteorite_landing_detail', kwargs={'pk': self.pk})
