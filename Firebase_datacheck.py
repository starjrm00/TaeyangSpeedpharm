import pandas as pd
from Firebase_connect import db

def datacheck():
    """
    Firestore Product 컬렉션과 날짜 서브컬렉션을 모두 가져와서
    pandas DataFrame으로 반환
    """
    products = []

    col_ref = db.collection("Product")
    docs = col_ref.stream()

    for doc in docs:
        print("docs의 doc세팅중")
        doc_data = doc.to_dict()
        doc_id = doc.id

        # 기본 필드
        거래처 = doc_data.get("거래처", "")
        상품명 = doc_data.get("상품명", "")
        규격 = doc_data.get("규격", "")
        출고가 = doc_data.get("출고가", 0)
        입고가 = doc_data.get("입고가", 0)
        기준약가 = doc_data.get("기준약가", 0)
        단위 = doc_data.get("단위", "")

        # 재고 dict(map) 가져오기
        # 한글 필드이므로 백틱 처리 가능
        snapshot = doc.reference.get(field_paths=["`재고`"])
        재고_dict = snapshot.to_dict().get("재고", {}) if snapshot.exists else {}

        # 날짜별로 분리
        print("날짜별 data분리중")
        for 날짜, 재고 in 재고_dict.items():
            products.append({
                "문서ID": doc_id,
                "거래처": 거래처,
                "상품명": 상품명,
                "규격": 규격,
                "출고가": 출고가,
                "입고가": 입고가,
                "기준약가": 기준약가,
                "단위": 단위,
                "날짜": 날짜,
                "재고": 재고
            })


    df = pd.DataFrame(products)
    return df

def get_product():
    print(db.project)
    col_ref = db.collection("Product")
    docs = col_ref.stream()
    rows = []

    for doc in docs:
        data = doc.to_dict()
        rows.append(data)

    return pd.DataFrame(rows)