import firebase_admin
import streamlit as st
import json
from firebase_admin import credentials, firestore
import pandas as pd
import os

#for local
#cred = credentials.Certificate("firebase_service_key.json")

#for distribution
cred = json.loads(st.secrets["firebase_service_key"])

try:
    firebase_admin.initialize_app(cred)
except:
    pass

db = firestore.client(database_id = "default")