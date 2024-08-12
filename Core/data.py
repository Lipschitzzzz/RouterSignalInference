import pandas as pd
def read(filepath):
    dataset = pd.read_excel(filepath)
    print(dataset)
read("data.xlsx")