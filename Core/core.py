import json
from . import intel_test

class Algorithm:
    def __init__(self):
        pass
    def parse(self):
        pass
    def run(self):
        pass

class Difference(Algorithm):
    def __init__(self, params):
        self.method = 'difference'
        self.params = params
        self.data = []
        # self.required_list = ['servPci', 'servRsrp', 'nbrPci_1', 'nbrRsrp_1', 'nbrPci_2', 'nbrRsrp_2',
                            #   'nbrPci_3', 'nbrRsrp_3', 'nbrPci_4', 'nbrRsrp_4', 'nbrPci_5', 'nbrRsrp_5']
        self.required_list = ['servRsrp', 'serv_x', 'serv_y', 'nbrRsrp_1', 'nbr_x_1', 'nbr_y_1',
                              'nbrRsrp_2', 'nbr_x_2', 'nbr_y_2','nbrRsrp_3', 'nbr_x_3', 'nbr_y_3',
                              'nbrRsrp_4', 'nbr_x_4', 'nbr_y_4','nbrRsrp_5', 'nbr_x_5', 'nbr_y_5',]
    def parse(self):
        for i in self.required_list:
            if self.params.get(i) != None:
                self.data.append(self.params[i])
            else:
                self.data.append(-1)
        k = len(self.data)
        for i in range(0, len(self.data), 3):
            self.data.append([self.data[i], self.data[i + 1], self.data[i + 2], 0])
        for i in range(0, k):
            self.data.pop(0)
                

    def run(self):
        # print(self.data)
        return intel_test.indoor_inf(self.data)
# /op-wireless/srs/report
'''
差分路损格式
[   [-72, 0.7, 8.6, 0],
    [-69, 8.2, 1.7, 0],
    [-71, 0.8, 13.6, 0],
    [-72, 8.2, 13.6, 0],
    [-72, 8.2, 7.6, 0],
    [-73, 2.2, 0.3, 0]  ]
    servrsrp x y unit
    nbr1rsrp x y unit
    ...
'''
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
    'ueId' : 1, 'servPci' : 1, 'servRsrp' : 1, 'servRsrq' : 1, 'servSinr' : 1, 'servTa' : 1, 'servRssi' : 1, 'servHaoa' : 1, 'servVaoa' : 1,
    'reserve_1' : 1, 'reserve_2' : 1,
    'nbrPci_1' : 1, 'nbrRsrp_1' : 1, 'nbrRsrq_1' : 1, 'nbrSinr_1' : 1, 'nbrvHaoa_1' : 1, 'nbrvHaoa_1' : 1,
    'nbrPci_2' : 1, 'nbrRsrp_2' : 1, 'nbrRsrq_2' : 1, 'nbrSinr_2' : 1, 'nbrvHaoa_2' : 1, 'nbrvHaoa_2' : 1,
    'nbrPci_3' : 1, 'nbrRsrp_3' : 1, 'nbrRsrq_3' : 1, 'nbrSinr_3' : 1, 'nbrvHaoa_3' : 1, 'nbrvHaoa_3' : 1,
    'nbrPci_4' : 1, 'nbrRsrp_4' : 1, 'nbrRsrq_4' : 1, 'nbrSinr_4' : 1, 'nbrvHaoa_4' : 1, 'nbrvHaoa_4' : 1,
    'nbrPci_5' : 1, 'nbrRsrp_5' : 1, 'nbrRsrq_5' : 1, 'nbrSinr_5' : 1, 'nbrvHaoa_5' : 1, 'nbrvHaoa_5' : 1
}
# m1 = Difference(data)
# m1.parse()
# result = m1.run()
# print(result)
# json_data = json.dumps(data)
# print(data)
# result = {}

# print(type(data))
# _data = []
# for i, j in data.items():
#     _data.append(j)
#     print(i, j)
# len_go = len(data)
# print(_data)
# print(indoor_inf(_data))

# 发送POST请求，并指定headers中的Content-Type为application/json
# response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'}, verify=False)
# 输出响应内容
# print(response.content)