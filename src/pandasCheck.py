import pandas as pd

df = pd.read_csv("TEST2.csv")

headers = list(df)


print(df.iloc[:,4].dtypes)