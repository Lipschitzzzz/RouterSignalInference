from django.shortcuts import render, redirect
from .models import LocationInfo, BaseStation, PciBaseStation, MobileBaseStation
import json
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from Core import intel_test, core

def query_info_by_ue_id(request, ue_id):
    if request.method == "GET":
        location_info = LocationInfo.objects.filter(ue_id = ue_id)
        if len(location_info) != 0:
            result = serialize("json", location_info)
            return HttpResponse(result, content_type = 'application/json')
    dict = [
    ]
    return HttpResponse(json.dumps(dict), content_type = 'application/json')

def query_info_all(request):
    if request.method == "GET":
        location_info = LocationInfo.objects.all()
        if len(location_info) != 0:
            result = serialize("json", location_info)
            return HttpResponse(result, content_type = 'application/json')
    dict = [
    ]
    return HttpResponse(json.dumps(dict), content_type = 'application/json')

def add_one_location_info(request):
    if request.method == "POST":
        seq_no = request.POST['seq_no']
        ue_id = request.POST['ue_id']

        serv_pci = request.POST['serv_pci']
        serv_rsrp = request.POST['serv_rsrp']
        serv_rsrq = request.POST['serv_rsrq']
        serv_sinr = request.POST['serv_sinr']
        serv_ta = request.POST['serv_ta']
        serv_rssi = request.POST['serv_rssi']

        reserve_1 = request.POST['reserve_1']
        reserve_2 = request.POST['reserve_2']

        nbr_pci_1 = request.POST['nbr_pci_1']
        nbr_rsrp_1 = request.POST['nbr_rsrp_1']
        nbr_rsrq_1 = request.POST['nbr_rsrq_1']
        nbr_sinr_1 = request.POST['nbr_sinr_1']

        nbr_pci_2 = request.POST['nbr_pci_2']
        nbr_rsrp_2 = request.POST['nbr_rsrp_2']
        nbr_rsrq_2 = request.POST['nbr_rsrq_2']
        nbr_sinr_2 = request.POST['nbr_sinr_2']

        nbr_pci_3 = request.POST['nbr_pci_3']
        nbr_rsrp_3 = request.POST['nbr_rsrp_3']
        nbr_rsrq_3 = request.POST['nbr_rsrq_3']
        nbr_sinr_3 = request.POST['nbr_sinr_3']

        nbr_pci_4 = request.POST['nbr_pci_4']
        nbr_rsrp_4 = request.POST['nbr_rsrp_4']
        nbr_rsrq_4 = request.POST['nbr_rsrq_4']
        nbr_sinr_4 = request.POST['nbr_sinr_4']

        nbr_pci_5 = request.POST['nbr_pci_5']
        nbr_rsrp_5 = request.POST['nbr_rsrp_5']
        nbr_rsrq_5 = request.POST['nbr_rsrq_5']
        nbr_sinr_5 = request.POST['nbr_sinr_5']

        if len(LocationInfo.objects.filter(ue_id = ue_id)) == 0:
            new_location_info = LocationInfo()
            new_location_info.seq_no = seq_no
            new_location_info.ue_id = ue_id

            new_location_info.serv_pci = serv_pci
            new_location_info.serv_rsrp = serv_rsrp
            new_location_info.serv_rsrq = serv_rsrq
            new_location_info.serv_sinr = serv_sinr
            new_location_info.serv_ta = serv_ta
            new_location_info.serv_rssi = serv_rssi

            new_location_info.reserve_1 = reserve_1
            new_location_info.reserve_2 = reserve_2

            new_location_info.nbr_pci_1 = nbr_pci_1
            new_location_info.nbr_rsrp_1 = nbr_rsrp_1
            new_location_info.nbr_rsrq_1 = nbr_rsrq_1
            new_location_info.nbr_sinr_1 = nbr_sinr_1

            new_location_info.nbr_pci_2 = nbr_pci_2
            new_location_info.nbr_rsrp_2 = nbr_rsrp_2
            new_location_info.nbr_rsrq_2 = nbr_rsrq_2
            new_location_info.nbr_sinr_2 = nbr_sinr_2

            new_location_info.nbr_pci_3 = nbr_pci_3
            new_location_info.nbr_rsrp_3 = nbr_rsrp_3
            new_location_info.nbr_rsrq_3 = nbr_rsrq_3
            new_location_info.nbr_sinr_3 = nbr_sinr_3

            new_location_info.nbr_pci_4 = nbr_pci_4
            new_location_info.nbr_rsrp_4 = nbr_rsrp_4
            new_location_info.nbr_rsrq_4 = nbr_rsrq_4
            new_location_info.nbr_sinr_4 = nbr_sinr_4

            new_location_info.nbr_pci_5 = nbr_pci_5
            new_location_info.nbr_rsrp_5 = nbr_rsrp_5
            new_location_info.nbr_rsrq_5 = nbr_rsrq_5
            new_location_info.nbr_sinr_5 = nbr_sinr_5

            new_location_info.save()
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
        msisdn = request.POST['msisdn']
        # base_station_id = request.POST['base_station_id'] # 小区 id
        imsi = request.POST['imsi']
        # if len(MobileBaseStation.objects.filter(msisdn = msisdn)) == 0:
            # new_mobile_base_station = MobileBaseStation(msisdn, base_station_id, imsi)
        new_mobile_base_station = MobileBaseStation()
        new_mobile_base_station.msisdn = msisdn
            # new_mobile_base_station.base_station_id = base_station_id
        new_mobile_base_station.imsi = imsi
        try:
            new_mobile_base_station.save()
            dict = [
                {'status': 200, 'message': 'Success'}
            ]
            return HttpResponse(json.dumps(dict), content_type = 'application/json')
        except:
            dict = [
            ]
            return HttpResponse(json.dumps(dict), content_type = 'application/json')

    dict = [
    ]
    return HttpResponse(json.dumps(dict), content_type = 'application/json')

def calculate_position(request, data):
    if request.method == "POST":
        data = json.loads(request.body)
        diff = core.Difference(data)
        diff.parse()
        result = diff.run()
        dict = [
             {'status': 200,
             'message': 'Success',
             'result' : result}
        ]
        return HttpResponse(json.dumps(dict), content_type = 'application/json')
    dict = [
    ]
    return HttpResponse(json.dumps(dict), content_type = 'application/json')