import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import os

cred = credentials.Certificate("firebase_service_key.json")
try:
    firebase_admin.initialize_app(cred)
except:
    pass

db = firestore.client(database_id = "default")

def get_product():
    print(db.project)
    col_ref = db.collection("Product")
    docs = col_ref.stream()
    rows = []

    for doc in docs:
        data = doc.to_dict()
        rows.append(data)

    return pd.DataFrame(rows)