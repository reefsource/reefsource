from django.contrib.gis import admin as gis_admin


class SecureOSM(gis_admin.OSMGeoAdmin):
    openlayers_url = 'https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'
