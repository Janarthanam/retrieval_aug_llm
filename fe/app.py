import os
import requests

import streamlit as st

BE = os.getenv("be_url")


datasets = requests.get(f"{BE}/v1/datasets", timeout=500).json()

st.sidebar.title("datasets")
ds = st.sidebar.selectbox(datasets)

query = st.text_input("Enter your search query")


answer = requests.post(f"http://localhost:8080/v1/datasets/{ds}", 
                       timeout=5000, json={'query': query} )

st.text = answer
