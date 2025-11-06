import pandas as pd
from Firebase_upload import upload_data
from Firebase_datacheck import datacheck
'''
df_pandas = get_product()
print(df_pandas)
for _, row in df_pandas.iterrows():
    upload_data(row)
'''

df_pandas = datacheck()
print(df_pandas)
