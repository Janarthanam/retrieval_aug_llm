import os
import requests

import streamlit as st

BE = os.getenv("be_url", "http://localhost:8080")

def get_answer(ds: str, query: str, llm: str) -> (str,dict):     
    res = requests.get(f"{BE}/v1/datasets/{ds}/answer?query={query}&llm={llm}", 
                        timeout=5000 ).json()
    return res["answer"], res["metadata"]

print(BE)
datasets = requests.get(f"{BE}/v1/datasets", timeout=500).json()

st.sidebar.title("Datasets")
ds = st.sidebar.selectbox(options=[ d["name"] for d in datasets], 
                          label="Select your dataset")
print(ds)
if ds:
    query = st.text_input("Enter your search query",
                          placeholder="Ask your question")
    if query:
        openai,openai_meta = get_answer(ds, query, "openai");
        llama,llama_meta = get_answer(ds, query, "llama2");

        st.write(f"openai: {openai}")
        st.write(f"llama: {llama}")

        files = [f"{f['file']}, page {f['page']}" for f in openai_meta]
        for fi in files:
            st.markdown(f"- {fi}")
else:
    st.write("Choose your dataset!")