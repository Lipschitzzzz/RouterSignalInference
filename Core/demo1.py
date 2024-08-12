import requests
import json
 
# 目标URL
url = 'https://lipschitz.pythonanywhere.com/op-wireless/srs/report'
# 请求的数据
data = {
    'seqNo' : 1,
    'timestamp' : "1721050662",
    'ueId' : 1, 'servPci' : 1, 'servRsrp' : -72, 'servRsrq' : 1, 'servSinr' : 1, 'servTa' : 1, 'servRssi' : 1, 'servHaoa' : 1, 'servVaoa' : 1,
    'reserve_1' : 1, 'reserve_2' : 1,
    'nbrPci_1' : 2, 'nbrRsrp_1' : -69, 'nbrRsrq_1' : 1, 'nbrSinr_1' : 1, 'nbrvHaoa_1' : 1, 'nbrvHaoa_1' : 1,
    'nbrPci_2' : 3, 'nbrRsrp_2' : -71, 'nbrRsrq_2' : 1, 'nbrSinr_2' : 1, 'nbrvHaoa_2' : 1, 'nbrvHaoa_2' : 1,
    'nbrPci_3' : 4, 'nbrRsrp_3' : -72, 'nbrRsrq_3' : 1, 'nbrSinr_3' : 1, 'nbrvHaoa_3' : 1, 'nbrvHaoa_3' : 1,
    'nbrPci_4' : 2, 'nbrRsrp_4' : -72, 'nbrRsrq_4' : 1, 'nbrSinr_4' : 1, 'nbrvHaoa_4' : 1, 'nbrvHaoa_4' : 1,
    'nbrPci_5' : 1, 'nbrRsrp_5' : -73, 'nbrRsrq_5' : 1, 'nbrSinr_5' : 1, 'nbrvHaoa_5' : 1, 'nbrvHaoa_5' : 1
}
json_data = json.dumps(data)
response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'}, verify=False)
print(response.content)