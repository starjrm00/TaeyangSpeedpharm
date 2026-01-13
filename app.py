import streamlit as st
import pandas as pd
from datetime import date
from XlsxToDataframe import xlsxToDf, makeNewProduct
from Firebase_upload import reduce_stock, undo_change, upload_new_data
from Firebase_datacheck import datacheck as get_product

st.set_page_config(page_title="재고 관리 시스템", layout="wide")
st.title("태양메디 재고관리 시스템")

#button 세팅
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    btn1 = st.button("DB편집창")
with col2:
    btn2 = st.button("비 약국 거래 + 약국 통합 조회창")
with col3:
    btn3 = st.button("약국 거래 조회창")
with col4:
    btn4 = st.button("세부 데이터 세팅창")
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
#1번 페이지 세팅 (엑셀 업로드)
if st.session_state.page == 1:
    
    st.markdown("DB업로드 페이지")
    with st.form("upload-form", clear_on_submit=True):
        uploaded_file = st.file_uploader("아래에 Speedpharm에서 받은 엑셀 파일을 업로드 해 주세요.", type=["xlsx"])
        submitted_upload = st.form_submit_button("업로드")
        if submitted_upload and uploaded_file is not None:
            df = xlsxToDf(uploaded_file)
            reduce_stock(df)
            st.success("해당 데이터가 DB에 적용되었습니다.")
        elif submitted_upload:
            st.error("엑셀 파일을 먼저 업로드해주세요")

    st.markdown("잘못 적용된 데이터 DB에서 되돌리기")
    with st.form("undo-form", clear_on_submit=True):
        undo_file = st.file_uploader("아래에 DB에 잘못 적용된 엑셀 파일을 업로드 해 주세요.", type=["xlsx"])
        submitted_undo = st.form_submit_button("업로드")
        if submitted_undo and undo_file is not None:
            df = xlsxToDf(undo_file)
            undo_change(df)
            st.success(f"잘못 반영되었던 해당 데이터가 수정되었습니다.\n해당 데이터의 이름은 <{undo_file.name}>입니다.")
        elif submitted_undo:
            st.error("엑셀 파일을 먼저 업로드해주세요")

elif st.session_state.page == 2:

    st.markdown("비약국 + 약국 통합 조회창")
    tmp_file = st.file_uploader("아래에 출력할 엑셀파일 업로드", type = ["xlsx"])

    if tmp_file is not None:
        df = xlsxToDf(tmp_file)
        st.success("엑셀 파일 업로드 완료")
        st.markdown("데이터 엑셀 형식으로 보기")
        st.dataframe(df, use_container_width=True)
        
        #edited_df = st.data_editor(
        #    df,
        #    use_container_width = True,
        #    num_rows="dynamic",
        #    hide_index = False,
        #    key="editable_table"
        #)

        #st.write("데이터 출력")
        #st.dataframe(edited_df.head(), use_container_width=True)
    else:
        st.info("엑셀 파일을 업로드 해주세요")

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
        거래처 = st.text_input("거래처", placeholder="예: 후문약국")
        상품명 = st.text_input("상품명", placeholder="예: 하모닐란액")
        규격 = st.text_input("규격", placeholder="예: 200mL")
        단위 = st.text_input("단위", placeholder="예: x개")
        출고가 = st.number_input("출고가", min_value=0, step=1)
        입고가 = st.number_input("입고가", min_value=0, step=1)
        기준약가 = st.number_input("기준약가", min_value=0, step=1)

        submitted = st.form_submit_button("데이터 생성")

        if submitted:
            if not all([거래처, 상품명, 규격, 단위]):
                st.error("모든 텍스틑 항목을 입력해주세요")
            elif 출고가 == 0 or 입고가 == 0 or 기준약가 == 0:
                st.error("거래 금액 관련 칸이 0입니다. 다시한번 확인해주세요")
            else:
                df = pd.DataFrame([{
                    "거래처": 거래처,
                    "상품명": 상품명,
                    "규격": 규격,
                    "단위": 단위,
                    "출고가": 출고가,
                    "입고가": 입고가,
                    "기준약가": 기준약가
                }])

                upload_new_data(df)
                st.success("해당 데이터가 DB에 적용되었습니다.")