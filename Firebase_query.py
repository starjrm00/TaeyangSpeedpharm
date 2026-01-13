from Firebase_connect import db
import pandas as pd

def query_transactions(store = None, product = None, size = None, start_date = None, end_date = None):
    product_ref = None
    if(store == None and product == None):
        product_ref = db.collection("Product").where("날짜", ">=", start_date).where("날짜", "<=", end_date)
    elif(store == None):
        product_ref = db.collection("Product").where("거래처", "==", store).where("날짜", ">=", start_date).where("날짜", "<=", end_date)
    elif(product == None):
        product_ref = db.collection("Product").where("상품명", "==", product).where("규격", "==", size).where("날짜", ">=", start_date).where("날짜", "<=", end_date)
    else:
        product_ref = db.collection("Product").where("거래처", "==", store).where("상품명", "==", product).where("규격", "==", size).where("날짜", ">=", start_date).where("날짜", "<=", end_date)

    