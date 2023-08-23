import os
import requests

import streamlit as st

BE = os.getenv("be_url")


datasets = requests.get(f"{BE}/v1/datasets", timeout=500).json()

st.sidebar.title("Datasets")
ds = st.sidebar.selectbox(options=[ d["name"] for d in datasets], 
                          label="Select your dataset")
print(ds)
if ds:
    query = st.text_input("Enter your search query",
                          placeholder="Ask your question")
    if query:
        res = requests.get(f"http://localhost:8080/v1/datasets/{ds}/answer?query={query}", 
                       timeout=5000 ).json()
        answer = res["answer"]

        st.write(answer)
        files = [f"{f['file']}, page {f['page']}" for f in res["metadata"]]
        for fi in files:
            st.markdown(f"- {fi}")
else:
    st.write("Choose your dataset!")