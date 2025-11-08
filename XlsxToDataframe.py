import pandas as pd

def xlsxToDf(xlsx):
    df_pandas = pd.read_excel(xlsx, header = 3)
    print(df_pandas.columns.tolist())

    #필요한 column만 추출하기
    df_pandas = df_pandas[["수불일자", "매출일자", "거래처", "상품명", "규격", "수량"]]
    df_pandas = df_pandas.dropna(subset = ["수불일자", "매출일자", "거래처", "상품명", "규격", "수량"])

    #날짜 data들 강제 형변환
    for col in ["수불일자", "매출일자"]:
        df_pandas[col] = pd.to_datetime(df_pandas[col], errors = "coerce")
    #diff_date_count = (df_pandas["수불일자"] != df_pandas["매출일자"]).sum()
    df_pandas = df_pandas[df_pandas["수불일자"] == df_pandas["매출일자"]]
    df_pandas["날짜"] = df_pandas["수불일자"]
    df_pandas = df_pandas.drop(columns=["수불일자", "매출일자"])
    print(df_pandas)
    return df_pandas