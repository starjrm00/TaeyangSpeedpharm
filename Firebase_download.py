from Firebase_connect import db
import pandas as pd

def get_pharmacy_data(start_date, end_date):
    """
    start_date, end_date : datetime.date
    return : pandas DataFrame
    
    :param start_date: Description
    :param end_date: Description
    """
    trade_ref = db.collection("Trade")
    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)

    query = trade_ref.where("date", ">=", start_ts).where("date", "<=", end_ts).where("is_pharmacy", "==", True)
    docs = query.stream()

    data_list = [doc.to_dict() for doc in docs]
    
    if not data_list:
        return pd.DataFrame()
    
    df = pd.DataFrame(data_list)
    cols = ["거래처", "상품명", "규격", "단위", "출고가", "입고가", "기준약가", "날짜", "판매량"]
    df = df[cols]
    return df