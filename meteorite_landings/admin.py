from django.contrib import admin

import meteorite_landings.models as models

# registering newly created models

@admin.register(models.Planet)
class PlanetAdmin(admin.ModelAdmin):
    fields = ["planet_name", "unsd_name"]
    list_display = ["planet_name", "unsd_name"]
    ordering = ["planet_name", "unsd_name"]

@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    fields = ["region_name"]
    list_display = ["region_name"]
    ordering = ["region_name"]

@admin.register(models.SubRegion)
class SubRegionAdmin(admin.ModelAdmin):
    fields = ["sub_region_name", "region"]
    list_display = ["sub_region_name", "region"]
    ordering = ["sub_region_name"]

@admin.register(models.IntermediateRegion)
class IntermediateRegion(admin.ModelAdmin):
    fields = ["intermediate_region_name", "sub_region"]
    list_display = ["intermediate_region_name", "sub_region"]
    ordering = ["intermediate_region_name"]

@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    fields = ["planet", "region", "sub_region", "intermediate_region"]
    list_display = ["planet", "region", "sub_region", "intermediate_region"]
    ordering = ["planet", "region", "sub_region", "intermediate_region"]

@admin.register(models.DevStatus)
class DevStatusAdmin(admin.ModelAdmin):
    fields = ["dev_status_name"]
    list_display = ["dev_status_name"]
    ordering = ["dev_status_name"]

@admin.register(models.CountryArea)
class CountryAreaAdmin(admin.ModelAdmin):
    fields = [
        "country_area_name",
        "m49_code",
        "iso_alpha3_code",
        "location",
        "dev_status"
    ]
    list_display = [
        "country_area_name",
        "m49_code",
        "iso_alpha3_code",
        "location",
        "dev_status"
    ]
    ordering = ["country_area_name"]
    list_filter = ["dev_status"]

@admin.register(models.MeteoriteClass)
class MeteoriteClassAdmin(admin.ModelAdmin):
    fields = [
        "code",
        "definition",
        "description"
    ]
    list_display = [
        "code",
        "definition",
        "description"
    ]
    ordering = ["code"]
