import pandas as pd
from Firebase_connect import get_product
from Firebase_upload import upload_data
from Firebase_datacheck import datacheck
'''
df_pandas = get_product()
print(df_pandas)
for _, row in df_pandas.iterrows():
    upload_data(row)
'''

df_pandas = pd.read_excel("./upload.xlsx", header = 3)
print(df_pandas.columns.tolist())

#날짜 data들 강제 형변환
for col in ["날짜"]:
    df_pandas[col] = pd.to_datetime(df_pandas[col], errors = "coerce")
print(df_pandas)

for _, row in df_pandas.iterrows():
    upload_data(row)