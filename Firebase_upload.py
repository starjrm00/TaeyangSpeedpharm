from Firebase_connect import db

def upload_new_data(row):
    doc_id = f"{row['거래처']}_{row['상품명']}_{row['규격']}"
    product_ref = db.collection("Product").document(doc_id)

    product_ref.set({
        "거래처": row["거래처"],
        "상품명": row["상품명"],
        "규격": row["규격"],
        "출고가": row["출고가"],
        "입고가": row["입고가"],
        "기준약가": row["기준약가"],
        "단위": row["단위"]
    }, merge = True)

    date_str = str(row["날짜"].date())

    snapshot = product_ref.get(field_paths=["`재고`"])    
    existing_stock = snapshot.to_dict().get("재고", {}) if snapshot.exists else {}

    current_stock = existing_stock.get(date_str, 0)
    existing_stock[date_str] = current_stock + row["재고"]

    product_ref.update({
        "재고": existing_stock
    })

def reduce_stock(df):
    '''
    for _, row in df.iterrows():
        doc_id = f"{row['거래처']}_{row['상품명']}_{row['규격']}"
        product_ref = db.collection("Product".document(doc_id))

        date_str = str(row['날짜'].date())

        snapshot = product_ref.get(field_paths=["`재고`"])    
        existing_stock = snapshot.to_dict().get("재고", {}) if snapshot.exists else {}

        current_stock = existing_stock.get(date_str, 0)
        existing_stock[date_str] = current_stock - row["수량"]

        product_ref.update({
            "재고": existing_stock
        })
        '''

def undo_change(df):
    for _, row in df.iterrows():
        doc_id = f"{row['거래처']}_{row['상품명']}_{row['규격']}"
        product_ref = db.collection("Product".document(doc_id))

        date_str = str(row['날짜'].date())

        snapshot = product_ref.get(field_paths=["`재고`"])    
        existing_stock = snapshot.to_dict().get("재고", {}) if snapshot.exists else {}

        current_stock = existing_stock.get(date_str, 0)
        existing_stock[date_str] = current_stock + row["수량"]

        product_ref.update({
            "재고": existing_stock
        })