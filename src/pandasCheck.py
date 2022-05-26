import pandas as pd
import os

df = pd.read_csv("TEST2.csv")

headers = list(df)
print(headers)
try:
    df['ID'] = df['ID'].fillna(0)
    df['ID'] = df['ID'].astype(float).astype('int64')
    print(df['ID'])
except Exception as ex:
    print(ex)