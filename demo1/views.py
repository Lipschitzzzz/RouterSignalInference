from django.shortcuts import render, redirect
from .models import Info, BaseStation, PciBaseStation, MobileBaseStation
import json
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse

def query_by_count_index(request, count_index):
    if request.method == "GET":
        info = Info.objects.filter(unsigned_message_count = count_index)
        if len(info) != 0:
            result = serialize("json", info)
            return HttpResponse(result, content_type = 'application/json')
    dict = [
    ]
    return HttpResponse(json.dumps(dict), content_type = 'application/json')

def query_all(request):
    if request.method == "GET":
        info = Info.objects.all()
        if len(info) != 0:
            result = serialize("json", info)
            return HttpResponse(result, content_type = 'application/json')
    dict = [
    ]
    return HttpResponse(json.dumps(dict), content_type = 'application/json')
    
def home_page(request):
    # dict = [
    #     {'id': 1, 'name': 'Ana'},
    #     {'id': 2, 'name': 'Bill'},
    # ]
    # return HttpResponse(json.dumps(dict), content_type = 'application/json')
    return render(request, 'home.html')


def en_register(request):
    if request.method == "POST":
        # enci = models.IntegerField(validators=[MinValueValidator(0)]) # 基站 id
        # pci = models.BigIntegerField(validators=[MinValueValidator(0)]) # 小区 id 改为外键
        # longitude = models.FloatField() # 经度
        # latitude = models.FloatField() # 纬度
        # height = models.FloatField() # 高度
        # azimuth = models.IntegerField(validators=[MinValueValidator(0)]) # 天线水平法线

        enci = request.POST['enci'] # 基站 id
        pci = request.POST['pci'] # 小区 id
        longitude = request.POST['longitude'] # 经度
        latitude = request.POST['latitude'] # 纬度
        height = request.POST['height'] # 高度
        azimuth = request.POST['azimuth'] # 天线水平法线方向
        # print(enci, pci, longitude, latitude, height, azimuth)

        if len(BaseStation.objects.filter(enci = enci)) == 0 and len(PciBaseStation.objects.filter(pci = pci)) == 0:
            # new_base_station = BaseStation(enci, longitude, latitude, height, azimuth)
            new_base_station = BaseStation()
            new_base_station.enci = enci
            new_base_station.longitude = longitude
            new_base_station.latitude = latitude
            new_base_station.height = height
            new_base_station.azimuth = azimuth
            new_base_station.save()

            # new_pci = PciBaseStation(pci, enci)
            new_pci = PciBaseStation()
            new_pci.pci = pci
            new_pci.base_station_id = new_base_station
            new_pci.save()
            dict = [
                {'status': 200, 'message': 'Success'}
            ]
            return HttpResponse(json.dumps(dict), content_type = 'application/json')
        else:
            dict = [
            ]
            return HttpResponse(json.dumps(dict), content_type = 'application/json')
    dict = [
    ]
    return HttpResponse(json.dumps(dict), content_type = 'application/json')

def ue_reg(request):
    if request.method == "POST":
        msisdn = request.POST['msisdn'] # 基站 id
        base_station_id = request.POST['base_station_id'] # 小区 id
        imsi = request.POST['imsi'] # 经度
        if len(MobileBaseStation.objects.filter(msisdn = msisdn, base_station_id = base_station_id)) != 0:
            # new_mobile_base_station = MobileBaseStation(msisdn, base_station_id, imsi)
            new_mobile_base_station = MobileBaseStation()
            new_mobile_base_station.msisdn = msisdn
            new_mobile_base_station.base_station_id = base_station_id
            new_mobile_base_station.imsi = imsi
            new_mobile_base_station.save()
            dict = [
                {'status': 200, 'message': 'Success'}
            ]
            return HttpResponse(json.dumps(dict), content_type = 'application/json')
        else:
            dict = [
            ]
            return HttpResponse(json.dumps(dict), content_type = 'application/json')

    dict = [
    ]
    return HttpResponse(json.dumps(dict), content_type = 'application/json')

