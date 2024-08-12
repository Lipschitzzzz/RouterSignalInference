import requests
import json
 
# 目标URL
url = 'https://lipschitz.pythonanywhere.com/op-wireless/gNB/properties/register'
# 请求的数据
data = {
    'gNB_ID' : 1,
    'pci' : 11,
    'axis' : 1,
    'longitude' : 1,
    'latitude' : 2,
    'height' : 3,
    'azimuth' : 4
}
json_data = json.dumps(data)
response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'}, verify=False)
print(response.content)