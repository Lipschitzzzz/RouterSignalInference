import pandas as pd
def read():
    dataset = pd.read_excel("data.xlsx")
    # print(dataset["height"][4])
    dataset.fillna(0.0, inplace=True)
    dataset.to_excel("data2.xlsx")
# read()