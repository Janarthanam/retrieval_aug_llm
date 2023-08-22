#!/bin/sh
python -m uvicorn "main:app" "--host" "0.0.0.0" "--port" "8080" &
python -m streamlit run app.py


 