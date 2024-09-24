import requests
import json
import urllib3

urllib3.disable_warnings()
# 目标URL
url = 'http://192.168.1.17:8000/op-wireless/srs/report'
# 请求的数据
data = {
    'seqNo' : 1,
    'timestamp' : "1721050662",
    'ueId' : 1, 'servPci' : 366, 'servRsrp' : -72, 'servRsrq' : 1, 'servSinr' : 1, 'servTa' : 1, 'servRssi' : 1, 'servHaoa' : 1, 'servVaoa' : 1,
    'reserve_1' : 1, 'reserve_2' : 1,
    'nbrPci_1' : 391, 'nbrRsrp_1' : -69, 'nbrRsrq_1' : 1, 'nbrSinr_1' : 1, 'nbrvHaoa_1' : 1, 'nbrvHaoa_1' : 1,
    'nbrPci_2' : 337, 'nbrRsrp_2' : -71, 'nbrRsrq_2' : 1, 'nbrSinr_2' : 1, 'nbrvHaoa_2' : 1, 'nbrvHaoa_2' : 1,
    'nbrPci_3' : 338, 'nbrRsrp_3' : -72, 'nbrRsrq_3' : 1, 'nbrSinr_3' : 1, 'nbrvHaoa_3' : 1, 'nbrvHaoa_3' : 1,
    'nbrPci_4' : 348, 'nbrRsrp_4' : -72, 'nbrRsrq_4' : 1, 'nbrSinr_4' : 1, 'nbrvHaoa_4' : 1, 'nbrvHaoa_4' : 1,
    'nbrPci_5' : 230, 'nbrRsrp_5' : -73, 'nbrRsrq_5' : 1, 'nbrSinr_5' : 1, 'nbrvHaoa_5' : 1, 'nbrvHaoa_5' : 1
}
# data = [[-72, 0.7, 8.6, 0],
#         [-69, 8.2, 1.7, 0],
#         [-71, 0.8, 13.6, 0],
#         [-72, 8.2, 13.6, 0],
#         [-72, 8.2, 7.6, 0],
#         [-73, 2.2, 0.3, 0]]
json_data = json.dumps(data)
response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'}, verify=False)
print(response.content)