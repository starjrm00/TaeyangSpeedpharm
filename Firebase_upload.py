from Firebase_connect import db
from google.cloud import firestore

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
            "pharmacy": is_pharmacy
        }, merge = True)

def upload_trade(df):
    missing_product = []
    product_cache = {}
    for _, row in df.iterrows():
        product_id = f"{row['거래처']}_{row['상품명']}_{row['규격']}".replace("/", "")
        trade_id = f"{row['거래처']}_{row['상품명']}_{row['규격']}_{row["날짜"]}".replace("/", "")

        if product_id not in product_cache:
            snapshot = db.collection("Product").document(product_id).get()
            if not snapshot.exists:
                print(f"상품이 없습니다. id : {product_id}")
                missing_product.append(product_id)
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
                "pharmacy": product["pharmacy"],
                "date": row["날짜"],
                "판매량": int(row["수량"])
            }
            trade_ref.set(trade_data)
    return missing_product

def undo_trade(df):
    product_cache = {}
    for _, row in df.iterrows():
        product_id = f"{row['거래처']}_{row['상품명']}_{row['규격']}".replace("/", "")
        trade_id = f"{row['거래처']}_{row['상품명']}_{row['규격']}_{row["날짜"]}".replace("/", "")

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
                "pharmacy": product["pharmacy"],
                "date": row["날짜"],
                "판매량": -int(row["수량"])
            }
            trade_ref.set(trade_data)

def edit_product_data(original_df, edited_df):
    product_ref = db.collection("Product")

    # 🔹 기존 doc_id 집합
    original_ids = set(original_df["doc_id"])

    # 🔹 수정된 doc_id 생성
    edited_df = edited_df.copy()
    edited_df["doc_id"] = (
        edited_df["거래처"] + "_"
        + edited_df["상품명"] + "_"
        + edited_df["규격"]
    )

    edited_ids = set(edited_df["doc_id"])

    # =========================
    # 1️⃣ 삭제 처리
    # =========================
    deleted_ids = original_ids - edited_ids

    for doc_id in deleted_ids:
        product_ref.document(doc_id).delete()

    # =========================
    # 2️⃣ 추가 + 수정 처리
    # =========================
    for _, row in edited_df.iterrows():

        doc_id = row["doc_id"]

        data = {
            "거래처": row["거래처"],
            "상품명": row["상품명"],
            "규격": row["규격"],
            "단위": row["단위"],
            "기준약가": row["기준약가"],
            "출고가": row["출고가"],
            "입고가": row["입고가"],
            "pharmacy": row.get("약국여부", False)
        }

        product_ref.document(doc_id).set(data)

    return True