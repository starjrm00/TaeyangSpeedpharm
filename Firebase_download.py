from Firebase_connect import db
import pandas as pd

def get_pharmacy_data(start_date, end_date):
    """
    start_date, end_date : datetime.date
    return : pandas DataFrame
    """
    trade_ref = db.collection("Trade")
    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)

    query = trade_ref.where("date", ">=", start_ts).where("date", "<=", end_ts).where("pharmacy", "==", True)
    docs = query.stream()

    data_list = [doc.to_dict() for doc in docs]
    
    if not data_list:
        return pd.DataFrame()
    
    df = pd.DataFrame(data_list)

    """
    if "date" in df.columns:
        df = df.rename(columns={"date": "날짜"})
        
    cols = ["거래처", "상품명", "규격", "단위", "출고가", "입고가", "기준약가", "날짜", "판매량"]
    df = df[cols]
    return df
    """

    df["거래내역"] = df["거래처"] + "_" + df["상품명"] + "_" + df["규격"]
    df["순매출"] = (df["출고가"] - df["입고가"]) * df["판매량"]
    #df["순매출"] = (df["출고가"] - df["입고가"]) * df["판매량"]

    cols = ["거래내역", "출고가", "입고가", "기준약가", "판매량", "순매출"]
    df = df[cols]

    grouped_df = (
        df.groupby("거래내역").agg(
            기준약가 = ("기준약가", "first"),
            출고가 = ("출고가", "first"),
            입고가 = ("입고가", "first"),
            판매량 = ("판매량", "sum"),
            순매출 = ("순매출", "sum")
        ).reset_index()
    )
    return grouped_df