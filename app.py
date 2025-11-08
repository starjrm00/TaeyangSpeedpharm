import streamlit as st
import pandas as pd
from datetime import date
from XlsxToDataframe import xlsxToDf
from Firebase_upload import reduce_stock
from Firebase_upload import undo_change
from Firebase_datacheck import datacheck as get_product

st.set_page_config(page_title="재고 관리 시스템", layout="wide")
st.title("태양메디 재고관리 시스템")

#button 세팅
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    btn1 = st.button("DB편집창")
with col2:
    btn2 = st.button("비 약국 거래 + 약국 통합 조회창")
with col3:
    btn3 = st.button("약국 거래 조회창")

#page 세팅
if 'page' not in st.session_state:
    st.session_state.page = 1

if btn1:
    st.session_state.page = 1
elif btn2:
    st.session_state.page = 2
elif btn3:
    st.session_state.page = 3

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