import firebase_admin
import streamlit as st
import json
from firebase_admin import credentials, firestore
import pandas as pd
import os

if os.path.exists("firebase_service_key.json"):
    #for local
    cred = credentials.Certificate("firebase_service_key.json")
else:
    #for release
    cred_dict = json.loads(st.secrets["firebase_service_key"])
    cred = credentials.Certificate(cred_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client(database_id = "default")