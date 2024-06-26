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

class LocationInfoAdmin(admin.ModelAdmin):
    list_display = ('seq_no', 'ue_id', 'serv_pci', 'serv_rsrp', 'serv_rsrq', 'serv_sinr', 'serv_ta', 'serv_rssi',
                    'reserve_1', 'reserve_2',
                    'nbr_pci_1', 'nbr_rsrp_1', 'nbr_rsrq_1', 'nbr_sinr_1',
                    'nbr_pci_2', 'nbr_rsrp_2', 'nbr_rsrq_2', 'nbr_sinr_2',
                    'nbr_pci_3', 'nbr_rsrp_3', 'nbr_rsrq_3', 'nbr_sinr_3',
                    'nbr_pci_4', 'nbr_rsrp_4', 'nbr_rsrq_4', 'nbr_sinr_4',
                    'nbr_pci_4', 'nbr_rsrp_4', 'nbr_rsrq_4', 'nbr_sinr_4',)
admin.site.register(LocationInfo, LocationInfoAdmin)
admin.site.register(BaseStation, BaseStationAdmin)
admin.site.register(PciBaseStation, PciBaseStationAdmin)
admin.site.register(MobileBaseStation)