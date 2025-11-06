import streamlit as st
import pandas as pd
from datetime import date
from Firebase_upload import upload_data
from Firebase_datacheck import datacheck as get_product
# 🔸 이미 구현되어 있다고 가정
# from your_firestore_module import upload_data, get_product

st.set_page_config(page_title="재고 관리 시스템", layout="wide")
st.title("태양메디 재고관리 시스템")

# --- 1️⃣ 엑셀 업로드 영역 ---
uploaded_file = st.file_uploader("📤 재고 데이터 엑셀 업로드 (xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success(f"엑셀 파일이 업로드되었습니다. ({len(df)}행)")
    
    # Firestore 반영
    if st.button("DB에 업로드"):
        upload_data(df)
        st.success("✅ 데이터가 Firestore에 업로드되었습니다.")

st.divider()

# --- 2️⃣ 검색 영역 ---
st.sidebar.header("🔍 검색 조건")

# 거래처 및 상품 검색 selectbox (get_product용으로 전달)
거래처 = st.sidebar.selectbox("거래처 선택", ["전체", "A상사", "B상사", "C상사"])  # 필요시 Firestore에서 목록 불러오기
상품 = st.sidebar.selectbox("상품명+규격 선택", ["전체", "제품1 500ml", "제품2 1L", "제품3 2L"])

# --- 3️⃣ 기간 설정 ---
st.sidebar.header("📅 기간 설정")
start_date = st.sidebar.date_input("시작일", date(2025, 1, 1))
end_date = st.sidebar.date_input("종료일", date.today())

# --- 4️⃣ 데이터 조회 ---
if st.sidebar.button("조회하기"):
    st.subheader("📋 조회 결과")

    # Firestore에서 조건에 맞는 데이터 가져오기
    result_df = get_product(거래처, 상품, start_date, end_date)

    if result_df is not None and not result_df.empty:
        st.dataframe(
            result_df.sort_values("날짜"),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("해당 조건에 맞는 데이터가 없습니다.")