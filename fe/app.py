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
        answer = requests.get(f"http://localhost:8080/v1/datasets/{ds}/answer?query={query}", 
                       timeout=5000 )

        print(answer.json()["answer"])
        st.write(answer.json()["answer"])
else:
    st.write("Choose your dataset!")