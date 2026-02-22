import streamlit as st
import pandas as pd
from datetime import date
from XlsxToDataframe import xlsxToDf, makeNewProduct
from Firebase_upload import upload_trade, undo_trade, upload_new_data, edit_product_data
from Firebase_download import get_pharmacy_data, get_all_data, get_product_data

st.set_page_config(page_title="재고 관리 시스템", layout="wide")
st.title("태양메디 재고관리 시스템")

#button 세팅
col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])
with col1:
    btn1 = st.button("거래내역 업로드")
with col2:
    btn2 = st.button("비 약국 거래 + 약국 통합 조회창")
with col3:
    btn3 = st.button("약국 거래 조회창")
with col4:
    btn4 = st.button("약품 데이터 업로드")
with col5:
    btn5 = st.button("약품 데이터 편집")
#page 세팅
if 'page' not in st.session_state:
    st.session_state.page = 1

if btn1:
    st.session_state.page = 1
elif btn2:
    st.session_state.page = 2
elif btn3:
    st.session_state.page = 3
elif btn4:
    st.session_state.page = 4
elif btn5:
    st.session_state.page = 5
#1번 페이지 세팅 (엑셀 업로드)
if st.session_state.page == 1:
    
    st.markdown("DB업로드 페이지")
    with st.form("upload-form", clear_on_submit=True):
        header = st.number_input("엑셀파일 위 필요 없는 줄 갯수", value=3)
        uploaded_file = st.file_uploader("아래에 Speedpharm에서 받은 엑셀 파일을 업로드 해 주세요.", type=["xlsx"])
        submitted_upload = st.form_submit_button("업로드")
        if submitted_upload and uploaded_file is not None:
            df = xlsxToDf(uploaded_file, header)
            missing = upload_trade(df)
            if missing:
                undo_trade(df)
                st.error("DB에 등록되지 않은 제품이 있어 DB 적용이 취소되었습니다.")
                for missing_product in missing:
                    st.error(f"{missing_product}상품이 상품 DB에 등록되지 않았습니다.")
            else:
                st.success("해당 데이터가 DB에 적용되었습니다.")
        elif submitted_upload:
            st.error("엑셀 파일을 먼저 업로드해주세요")

    st.markdown("잘못 적용된 데이터 DB에서 되돌리기")
    with st.form("undo-form", clear_on_submit=True):
        header = st.number_input("엑셀파일 위 필요 없는 줄 갯수", value=3)
        undo_file = st.file_uploader("아래에 DB에 잘못 적용된 엑셀 파일을 업로드 해 주세요.", type=["xlsx"])
        submitted_undo = st.form_submit_button("업로드")
        if submitted_undo and undo_file is not None:
            df = xlsxToDf(undo_file, header)
            undo_trade(df)
            st.success(f"잘못 반영되었던 해당 데이터가 수정되었습니다.\n해당 데이터의 이름은 <{undo_file.name}>입니다.")
        elif submitted_undo:
            st.error("엑셀 파일을 먼저 업로드해주세요")

elif st.session_state.page == 2:

    st.markdown("비약국 + 약국 통합 거래 조회")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("시작 날짜")
    with col2:
        end_date = st.date_input("종료 날짜")

    if st.button("조회하기"):
        if start_date > end_date:
            st.error("시작 날짜는 종료 날짜보다 뒤일 수 없습니다.")
        else:
            df = get_all_data(start_date, end_date)

            if df.empty:
                st.info("기간 내 약국 거래 데이터가 존재하지 않습니다.")
            else:
                st.success(f"{len(df)-2}개의 비약국 거래내역 존재")
                df.index = df.index+1
                st.dataframe(df.style.set_properties(subset=["판매량", "순매출"],**{"background-color": "#FFF3B0"}), use_container_width=True)

elif st.session_state.page == 3:
    st.markdown("약국 거래 조회")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("시작 날짜")
    with col2:
        end_date = st.date_input("종료 날짜")

    if st.button("조회하기"):
        if start_date > end_date:
            st.error("시작 날짜는 종료 날짜보다 뒤일 수 없습니다.")
        else:
            df = get_pharmacy_data(start_date, end_date)

            if df.empty:
                st.info("기간 내 약국 거래 데이터가 존재하지 않습니다.")
            else:
                st.success(f"{len(df)-1}개의 거래내역 존재")
                df.index = df.index+1
                st.dataframe(df.style.set_properties(subset=["판매량", "순매출"],**{"background-color": "#FFF3B0"}), use_container_width=True)

elif st.session_state.page == 4:

    st.markdown("상품 기본 데이터 입력")

    with st.form("upload-form", clear_on_submit=True):
        uploaded_file = st.file_uploader("데이터를 설정할 엑셀파일을 업로드 해주세요", type=["xlsx"])
        submitted_upload = st.form_submit_button("업로드")
        if submitted_upload and uploaded_file is not None:
            df = makeNewProduct(uploaded_file)
            upload_new_data(df)
            st.success("해당 데이터가 DB에 적용되었습니다.")
        elif submitted_upload:
            st.error("엑셀 파일을 먼저 업로드해주세요")

    with st.form("product input form"):
        st.markdown("직접 하나씩 입력하기")
        st.text("거래처, 상품명, 규격 3개가 모두 동일할 시 같은 데이터로 취급해서 값이 덮어씌워집니다.")
        거래처 = st.text_input("거래처", placeholder="예: 후문약국")
        상품명 = st.text_input("상품명", placeholder="예: 하모닐란액")
        규격 = st.text_input("규격", placeholder="예: 200mL")
        단위 = st.text_input("단위", placeholder="예: x개")
        출고가 = st.number_input("출고가", min_value=-1, step=1, value=-1)
        입고가 = st.number_input("입고가", min_value=-1, step=1, value=-1)
        기준약가 = st.number_input("기준약가", min_value=-1, step=1, value=-1)
        분류 = st.radio(
            "거래처 분류 선택",
            ["약국", "도매", "종합병원"],
            horizontal=True
        )

        submitted = st.form_submit_button("데이터 생성")

        if submitted:
            if not all([거래처, 상품명, 규격, 단위]):
                st.error("모든 텍스틑 항목을 입력해주세요")
            elif 출고가 < 0 or 입고가 < 0 or 기준약가 < 0:
                st.error("거래 금액 관련 칸이 음수입니다. 다시한번 확인해주세요")
            else:
                df = pd.DataFrame([{
                    "거래처": 거래처,
                    "상품명": 상품명,
                    "규격": 규격,
                    "단위": 단위,
                    "출고가": 출고가,
                    "입고가": 입고가,
                    "기준약가": 기준약가,
                    "기능": 분류
                }])

                upload_new_data(df)
                st.success("해당 데이터가 DB에 적용되었습니다.")
elif st.session_state.page == 5:
    original_df = get_product_data()
    if original_df.empty:
        st.info("약품 데이터를 불러오는데 오류가 발생했습니다.")

    else:
        display_df = original_df.drop(columns=["doc_id"], errors = 'ignore')
        edited_df = st.data_editor(
            display_df,
            num_rows = "dynamic",
            use_container_width=True,
            key = "product_editor"
        )
        if st.button("수정사항 저장"):
            success = edit_product_data(original_df, edited_df)

            if success:
                st.session_state["edit_product_success"] = True
        if st.session_state.get("edit_product_success"):
            st.success("수정사항 반영이 완료되었습니다.")
            del st.session_state["edit_product_success"]