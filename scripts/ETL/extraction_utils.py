import pandas as pd

def extract_data_xlsx(file_path):
    data = pd.read_excel(file_path)
    print(data.shape)
    return data


def extract_data_csv(file_path):
    data = pd.read_csv(file_path)
    print(data.shape)
    return data