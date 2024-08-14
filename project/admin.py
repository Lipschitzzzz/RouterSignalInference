from typing import Any
from django.contrib import admin
from .models import *
import pandas as pd
from Backend import settings
import os
import platform

# Register your models here.

class BaseStationAdmin(admin.ModelAdmin):
    list_display = ('gNB_ID', 'axis', 'longitude', 'latitude', 'height', 'azimuth') # list
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
    list_display = ('pci', 'base_station_id__gNB_ID')
    def base_station_id__gNB_ID(self, obj):
        return obj.base_station_id.gNB_ID

class LocationInfoAdmin(admin.ModelAdmin):
    list_display = ('seq_no', 'ue_id', 'serv_pci', 'serv_rsrp', 'serv_rsrq', 'serv_sinr', 'serv_ta', 'serv_rssi',
                    'reserve_1', 'reserve_2',
                    'nbr_pci_1', 'nbr_rsrp_1', 'nbr_rsrq_1', 'nbr_sinr_1',
                    'nbr_pci_2', 'nbr_rsrp_2', 'nbr_rsrq_2', 'nbr_sinr_2',
                    'nbr_pci_3', 'nbr_rsrp_3', 'nbr_rsrq_3', 'nbr_sinr_3',
                    'nbr_pci_4', 'nbr_rsrp_4', 'nbr_rsrq_4', 'nbr_sinr_4',
                    'nbr_pci_4', 'nbr_rsrp_4', 'nbr_rsrq_4', 'nbr_sinr_4',)

class DataManagerAdmin(admin.ModelAdmin):
    list_display = ('file', 'relative_path', 'add_date')
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        relative_path = str(obj.relative_path)
        file = str(obj.file)
        # path = settings.BASE_DIR + '/' + obj.relative_path + '/' + str(obj.file)
        # if platform.system() == "Windows":
            # path.replace("/", "\\")
        # print(path)
        # path = str(obj)
        super().save_model(request, obj, form, change)
        # print("../"+relative_path+file)
        try:
            dataset = pd.read_excel("media/"+relative_path+"/"+file)
            for i in range(0, len(dataset)):
                gNB_ID = int(dataset["enci"][i])
                base_info = BaseStation.objects.filter(gNB_ID = gNB_ID)
                if len(base_info) == 0:
                    new_base_station = BaseStation()
                    new_base_station.gNB_ID = gNB_ID
                    new_base_station.axis = 0
                    new_base_station.longitude = dataset["wgs84_x"][i]
                    new_base_station.latitude = dataset["wgs84_y"][i]
                    new_base_station.height = dataset["height"][i]
                    new_base_station.azimuth = int(dataset["azimuth"][i])
                    new_base_station.save()
                    new_pci = PciBaseStation()
                    new_pci.pci = int(dataset["pci"][i])
                    new_pci.base_station_id = new_base_station
                    new_pci.save()
                    print("Base created and pci linked successfully")
                else:
                    new_pci = PciBaseStation()
                    new_pci.pci = int(dataset["pci"][i])
                    new_pci.base_station_id = base_info[0]
                    print("Pci linked successfully")
        except:
            print("Unexpected error please check your data format")
        return None

    
class UEInformationAdmin(admin.ModelAdmin):
    list_display = ('ueid', 'x', 'y', 'mod_date')

# admin.site.register(LocationInfo, LocationInfoAdmin)
admin.site.register(BaseStation, BaseStationAdmin)
admin.site.register(PciBaseStation, PciBaseStationAdmin)
# admin.site.register(MobileBaseStation)
admin.site.register(UEInformation, UEInformationAdmin)
admin.site.register(DataManager, DataManagerAdmin)

#admin.site.register(LocationInfo, LocationInfoAdmin)
# admin.site.register(BaseStation, BaseStationAdmin)
# admin.site.register(PciBaseStation, PciBaseStationAdmin)
#admin.site.register(MobileBaseStation)
