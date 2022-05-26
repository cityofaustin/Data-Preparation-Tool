import pandas as pd
import os

df = pd.read_csv("TEST2.csv")

headers = list(df)


print(df.iloc[:,4].dtypes)
print(os.path.dirname(__file__))