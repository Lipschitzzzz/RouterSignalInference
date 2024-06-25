from django.contrib import admin
from .models import *

# Register your models here.
 
class BaseStationAdmin(admin.ModelAdmin):
    list_display = ('enci','longitude', 'longitude', 'latitude', 'height', 'azimuth') # list
    # fieldsets = (
    #     ['Main',{
    #         'fields':('name','email'),
    #     }],
    #     ['Advance',{
    #         'classes': ('collapse',),
    #         'fields': ('age',),
    #     }]
 
    # )

class PciBaseStationAdmin(admin.ModelAdmin):
    list_display = ('pci', 'base_station_id__enci')
    def base_station_id__enci(self, obj):
        return obj.base_station_id.enci

class InfoAdmin(admin.ModelAdmin):
    list_display = ('unsigned_message_count','ue_id', 'pci_0', 'rsrp_0') # list

admin.site.register(Info, InfoAdmin)
admin.site.register(BaseStation, BaseStationAdmin)
admin.site.register(PciBaseStation, PciBaseStationAdmin)
admin.site.register(MobileBaseStation)