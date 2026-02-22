from Firebase_connect import db
import pandas as pd

def get_pharmacy_data(start_date, end_date):
    df = get_data(start_date, end_date, True)
    total_row = pd.DataFrame({
        "거래내역": ["합계"],
        "기준약가" : [None],
        "출고가" : [None],
        "입고가" : [None],
        "판매량" : [df["판매량"].sum()],
        "순매출" : [df["순매출"].sum()]
    })

    df = pd.concat([df, total_row], ignore_index = True)

    return df

def get_all_data(start_date, end_date):
    df_non_pharmacy = get_data(start_date, end_date, False)
    df_pharmacy = get_data(start_date, end_date, True)
    
    pharmacy_row = pd.DataFrame({
        "거래내역": ["약국"],
        "기준약가" : [None],
        "출고가" : [None],
        "입고가" : [None],
        "판매량" : [df_pharmacy["판매량"].sum()],
        "순매출" : [df_pharmacy["순매출"].sum()]
    })
    df = pd.concat([df_non_pharmacy, pharmacy_row], ignore_index = True)

    total_row = pd.DataFrame({
        "거래내역": ["합계"],
        "기준약가" : [None],
        "출고가" : [None],
        "입고가" : [None],
        "판매량" : [df["판매량"].sum()],
        "순매출" : [df["순매출"].sum()]
    })
    df = pd.concat([df, total_row], ignore_index = True)
    return df

def get_data(start_date, end_date, pharmacy):
    """
    start_date, end_date : datetime.date
    return : pandas DataFrame
    """
    trade_ref = db.collection("Trade")
    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)

    query = trade_ref.where("date", ">=", start_ts).where("date", "<=", end_ts).where("pharmacy", "==", pharmacy)
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
        df.groupby(["거래내역", "기준약가", "출고가", "입고가"]).agg(
            판매량 = ("판매량", "sum"),
            순매출 = ("순매출", "sum")
        ).reset_index()
    )

    return grouped_df

def get_product_data():
    product_ref = db.collection("Product")
    docs = product_ref.stream()
    data_list = []
    for doc in docs:
        item = doc.to_dict()
        item["doc_id"] = doc.id
        data_list.append(item)

    df = pd.DataFrame(data_list)
    df = df.rename(columns={"pharmacy": "약국여부"})
    df = df[["doc_id", "거래처", "상품명", "규격", "단위", "기준약가", "출고가", "입고가", "약국여부"]]
    #df = df[["doc_id", "거래처", "상품명", "규격", "단위", "기준약가", "출고가", "입고가"]]
    return df