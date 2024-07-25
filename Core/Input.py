import requests
import json
 
# 目标URL
url = 'https://lipschitz.pythonanywhere.com/op-wireless/srs/report'
# url = 'http://127.0.0.1:8000/test/ue/register'
# /op-wireless/srs/report
# 请求的数据
# data = {
#         'serv' : [-72, 0.7, 8.6, 0],
#         'nbr1' : [-69, 8.2, 1.7, 0],
#         'nbr2' : [-71, 0.8, 13.6, 0],
#         'nbr3' : [-72, 8.2, 13.6, 0],
#         'nbr4' : [-72, 8.2, 7.6, 0],
#         'nbr5' : [-73, 2.2, 0.3, 0]
#         }
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

# 跑十次 取平均
# 取平均 跑一次 rsrp

# ueid = x 从第一条开始 10s后返回 x 这一条
json_data = json.dumps(data)
# print(sp.version)
# print(json_data)
print(data)
result = {}
# result['2'] = 3
# print(result)

print(type(data))
_data = []
for i, j in data.items():
    _data.append(j)
    print(i, j)
len_go = len(data)
print(_data)
# print(indoor_inf(_data))

# 发送POST请求，并指定headers中的Content-Type为application/json
response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'}, verify=False)
# 输出响应内容
print(response.content)