import intel_test
data = [[-72, 0.7, 8.6, 0],
        [-69, 8.2, 1.7, 0],
        [-71, 0.8, 13.6, 0],
        [-72, 8.2, 13.6, 0],
        [-72, 8.2, 7.6, 0],
        [-73, 2.2, 0.3, 0]]

# result = indoor_inf(data)
# print(result)

result = intel_test.indoor_inf(data)
print(result)