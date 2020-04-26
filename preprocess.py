import pandas as pd

if __name__ == "__main__":
    dataframe = pd.read_csv("data_combined.csv", low_memory=False)
    print(dataframe.columns)
    print(dataframe.head())
    print(dataframe.describe())