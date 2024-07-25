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


# 基站工参注册
def gNB_ID_pci_register(request):
    try:
        data = json.loads(request.body)
        data_list = []
        temp = ['gNB_ID', 'pci', 'axis', 'longitude',
                'latitude', 'height', 'azimuth']
        for i in temp:
            if data.get(i) != None:
                data_list.append(data[i])
            else:
                data_list.append(0)
        # gNB_ID = request.POST['gNB_ID'] # 基站 id
        # pci = request.POST['pci'] # 小区 id
        # axis = request.POST['axis']
        # longitude = request.POST['longitude'] # 经度
        # latitude = request.POST['latitude'] # 纬度
        # height = request.POST['height'] # 高度
        # azimuth = request.POST['azimuth'] # 天线水平法线方向
        gNB_ID = data_list['gNB_ID']
        pci = data_list['pci']
        axis = data_list['axis']
        longitude = data_list['longitude']
        latitude = data_list['latitude']
        height = data_list['height']
        azimuth = data_list['azimuth']

        # 基站已注册过，直接绑定小区
        base = BaseStation.objects.filter(gNB_ID = gNB_ID)
        if len(base) == 0:
            new_pci = PciBaseStation()
            new_pci.pci = pci
            new_pci.base_station_id = base
            new_pci.save()
            dict = [
                {'status': 200,
                 'message': 'base has been registered successfully'}
            ]
            return HttpResponse(json.dumps(dict), content_type = 'application/json')
        # 基站还未注册，先注册基站，再绑定小区
        else:
            new_base_station = BaseStation()
            new_base_station.gNB_ID = gNB_ID
            new_base_station.axis = axis
            new_base_station.longitude = longitude
            new_base_station.latitude = latitude
            new_base_station.height = height
            new_base_station.azimuth = azimuth
            new_base_station.save()

            new_pci = PciBaseStation()
            new_pci.pci = pci
            new_pci.base_station_id = new_base_station
            new_pci.save()
            dict = [
                {'status': 200,
                 'message': 'base has been registered successfully'}
            ]
            return HttpResponse(json.dumps(dict), content_type = 'application/json')
    except json.JSONDecodeError:
        # dict = [
            # {
                # 'status': 500,
                # 'message': 'Unknown Error'}
            # ]
        # return HttpResponse(json.dumps(dict), content_type = 'application/json')
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
'''
    if request.method == "POST":

        gNB_ID = request.POST['gNB_ID'] # 基站 id
        pci = request.POST['pci'] # 小区 id
        axis = request.POST['axis']
        longitude = request.POST['longitude'] # 经度
        latitude = request.POST['latitude'] # 纬度
        height = request.POST['height'] # 高度
        azimuth = request.POST['azimuth'] # 天线水平法线方向

        # 基站已注册过，直接绑定小区
        base = BaseStation.objects.filter(gNB_ID = gNB_ID)
        if len(base) == 0:
            new_pci = PciBaseStation()
            new_pci.pci = pci
            new_pci.base_station_id = base
            new_pci.save()
            dict = [
                {'status': 200,
                 'message': 'base has been registered successfully'}
            ]
            return HttpResponse(json.dumps(dict), content_type = 'application/json')
        # 基站还未注册，先注册基站，再绑定小区
        else:
            new_base_station = BaseStation()
            new_base_station.gNB_ID = gNB_ID
            new_base_station.axis = axis
            new_base_station.longitude = longitude
            new_base_station.latitude = latitude
            new_base_station.height = height
            new_base_station.azimuth = azimuth
            new_base_station.save()

            new_pci = PciBaseStation()
            new_pci.pci = pci
            new_pci.base_station_id = new_base_station
            new_pci.save()
            dict = [
                {'status': 200,
                 'message': 'base has been registered successfully'}
            ]
            return HttpResponse(json.dumps(dict), content_type = 'application/json')
    dict = [
        {'status': 500,
         'message': 'Unknown Error'}
    ]
    return HttpResponse(json.dumps(dict), content_type = 'application/json')
'''



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


# serv和nbr 任意一个查不到 直接return error
# 有rsrq和sinr（任意一个） -> 指纹库
# 有Vaoa和Haoa -> Aoa算法
# 基站注册信息修改
def calculate_position(request):
    try:
        data = json.loads(request.body)
        pci_list = []
        temp = ['servPci', 'nbrPci_1', 'nbrPci_2', 'nbrPci_3',
                'nbrPci_4', 'nbrPci_5']
        for i in temp:
            if data.get(i) != None:
                pci_list.append(data[i])
            else:
                pci_list.append(-1)
        # print(pci_list)
        required_list = [['serv_x', 'serv_y'], ['nbr_x_1', 'nbr_y_1'],
                            ['nbr_x_2', 'nbr_y_2'], ['nbr_x_3', 'nbr_y_3'],
                            ['nbr_x_4', 'nbr_y_4'], ['nbr_x_5', 'nbr_y_5']]
        for i in range(0, len(pci_list)):
            gNB_ID = PciBaseStation.objects.filter(pci = pci_list[i])
            # print(enci[0])
            if len(gNB_ID) != 0:
                data[required_list[i][0]] = gNB_ID[0].base_station_id.longitude
                data[required_list[i][1]] = gNB_ID[0].base_station_id.latitude
            else:
                data[required_list[i][0]] = -1
                data[required_list[i][1]] = -1
        # print(data)
        diff = core.Difference(data)
        diff.parse()
        result = diff.run()
        # print(result)
        dict = [
            {
                 'status': 200,
                 'message': 'Success',
                 'result' : result
            }
        ]
        return HttpResponse(json.dumps(dict), content_type = 'application/json')
        # return JsonResponse({'status': 'success', 'data': data})
    except json.JSONDecodeError:
        # dict = [
            # {
                # 'status': 500,
                # 'message': 'Unknown Error'}
            # ]
        # return HttpResponse(json.dumps(dict), content_type = 'application/json')
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    



'''
    if request.method == "GET":
        data = {
        'seqNo' : 1,
        'timestamp' : "1721050662",
        'ueId' : 1, 'servPci' : 1, 'servRsrp' : -72, 'servRsrq' : 1, 'servSinr' : 1, 'servTa' : 1, 'servRssi' : 1, 'servHaoa' : 1, 'servVaoa' : 1,
        'reserve_1' : 1, 'reserve_2' : 1,
        'nbrPci_1' : 2, 'nbrRsrp_1' : -69, 'nbrRsrq_1' : 1, 'nbrSinr_1' : 1, 'nbrvHaoa_1' : 1, 'nbrvHaoa_1' : 1,
        'nbrPci_2' : 3, 'nbrRsrp_2' : -71, 'nbrRsrq_2' : 1, 'nbrSinr_2' : 1, 'nbrvHaoa_2' : 1, 'nbrvHaoa_2' : 1,
        'nbrPci_3' : 4, 'nbrRsrp_3' : -72, 'nbrRsrq_3' : 1, 'nbrSinr_3' : 1, 'nbrvHaoa_3' : 1, 'nbrvHaoa_3' : 1,
        'nbrPci_4' : 5, 'nbrRsrp_4' : -72, 'nbrRsrq_4' : 1, 'nbrSinr_4' : 1, 'nbrvHaoa_4' : 1, 'nbrvHaoa_4' : 1,
        'nbrPci_5' : 6, 'nbrRsrp_5' : -73, 'nbrRsrq_5' : 1, 'nbrSinr_5' : 1, 'nbrvHaoa_5' : 1, 'nbrvHaoa_5' : 1
                }
        json_data = json.dumps(data)
        json_data_load = json.loads(json_data)
        l1 = []
        temp = ['servPci', 'nbrPci_1', 'nbrPci_2', 'nbrPci_3',
                'nbrPci_4', 'nbrPci_5']
        for i in temp:
            if json_data_load.get(i) != None:
                l1.append(json_data_load[i])
            else:
                l1.append(-1)
        # print(l1)
        required_list = [['serv_x', 'serv_y'], ['nbr_x_1', 'nbr_y_1'],
                            ['nbr_x_2', 'nbr_y_2'], ['nbr_x_3', 'nbr_y_3'],
                            ['nbr_x_4', 'nbr_y_4'], ['nbr_x_5', 'nbr_y_5']]
        for i in range(0, len(l1)):
            gNB_ID = PciBaseStation.objects.filter(pci = l1[i])
            # print(enci[0])
            if len(gNB_ID) != 0:
                data[required_list[i][0]] = gNB_ID[0].base_station_id.longitude
                data[required_list[i][1]] = gNB_ID[0].base_station_id.latitude
            else:
                data[required_list[i][0]] = -1
                data[required_list[i][1]] = -1
        # print(data)
        diff = core.Difference(data)
        diff.parse()
        result = diff.run()
        # print(result)
        dict = [
            {
                 'status': 200,
                 'message': 'Success',
                 'result' : result
            }
        ]
        return HttpResponse(json.dumps(dict), content_type = 'application/json')


    # if request.method == "POST":
    #     data = json.loads(request.body)
    #     diff = core.Difference(data)
    #     diff.parse()
    #     result = diff.run()
    #     dict = [
    #          {'status': 200,
    #          'message': 'Success',
    #          'result' : result}
    #     ]
    #     return HttpResponse(json.dumps(dict), content_type = 'application/json')
    dict = [
        {'status': 500,
         'message': 'Unknown Error'}
    ]
    return HttpResponse(json.dumps(dict), content_type = 'application/json')
'''