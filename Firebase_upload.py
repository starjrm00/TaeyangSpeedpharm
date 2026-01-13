from Firebase_connect import db

def upload_new_data(df):
    for _, row in df.iterrows():
        doc_id = f"{row['거래처']}_{row['상품명']}_{row['규격']}".replace("/", "")
        product_ref = db.collection("Product").document(doc_id)

        is_pharmacy = "약국" in row["거래처"]

        product_ref.set({
            "거래처": row["거래처"],
            "상품명": row["상품명"],
            "규격": row["규격"],
            "출고가": row["출고가"],
            "입고가": row["입고가"],
            "기준약가": row["기준약가"],
            "단위": row["단위"],
            "약국": is_pharmacy
        }, merge = True)

def upload_trade(df):
    product_cache = {}
    for _, row in df.iterrows():
        date_str = str(row['날짜'].date())
        product_id = f"{row['거래처']}_{row['상품명']}_{row['규격']}".replace("/", "")
        trade_id = f"{row['거래처']}_{row['상품명']}_{row['규격']}_{date_str}".replace("/", "")

        if product_id not in product_cache:
            snapshot = db.collection("Product").document(product_id).get()
            if not snapshot.exists:
                print(f"상품이 없습니다. id : {product_id}")
                continue
            product_cache[product_id] = snapshot.to_dict()

        product = product_cache[product_id]

        trade_ref = db.collection("Trade").document(trade_id)
        trade_snapshot = trade_ref.get()
        if trade_snapshot.exists:
            existing_data = trade_snapshot.to_dict()
            existing_transaction = existing_data.get("판매량", 0)
            new_transaction = existing_transaction + int(row["수량"])
            trade_ref.update({"판매량": new_transaction})
        else:
            trade_data = {
                "거래처": product["거래처"],
                "상품명": product["상품명"],
                "규격": product["규격"],
                "단위": product["단위"],
                "출고가": product["출고가"],
                "입고가": product["입고가"],
                "기준약가": product["기준약가"],
                "약국": product["약국"],
                "날짜": date_str,
                "판매량": int(row["수량"])
            }
            trade_ref.set(trade_data)

def undo_trade(df):
    product_cache = {}
    for _, row in df.iterrows():
        date_str = str(row['날짜'].date())
        product_id = f"{row['거래처']}_{row['상품명']}_{row['규격']}".replace("/", "")
        trade_id = f"{row['거래처']}_{row['상품명']}_{row['규격']}_{date_str}".replace("/", "")

        if product_id not in product_cache:
            snapshot = db.collection("Product").document(product_id).get()
            if not snapshot.exists:
                print(f"상품이 없습니다. id : {product_id}")
                continue
            product_cache[product_id] = snapshot.to_dict()

        product = product_cache[product_id]

        trade_ref = db.collection("Trade").document(trade_id)
        trade_snapshot = trade_ref.get()
        if trade_snapshot.exists:
            existing_data = trade_snapshot.to_dict()
            existing_transaction = existing_data.get("판매량", 0)
            new_transaction = existing_transaction - int(row["수량"])
            trade_ref.update({"판매량": new_transaction})
        else:
            trade_data = {
                "거래처": product["거래처"],
                "상품명": product["상품명"],
                "규격": product["규격"],
                "단위": product["단위"],
                "출고가": product["출고가"],
                "입고가": product["입고가"],
                "기준약가": product["기준약가"],
                "약국": product["약국"],
                "날짜": date_str,
                "판매량": -int(row["수량"])
            }
            trade_ref.set(trade_data)