#!/bin/bash
python -m uvicorn "main:app" "--host" "0.0.0.0" "--port" "8080" &
python3 -m celery -A worker.celery worker --loglevel=debug &

#active wait- container won't quit
while ! timeout 1 bash -c "echo > /dev/tcp/localhost/8080"; do sleep 5; done

export be_url=`awk 'END{print "http://"$1":8080"}' /etc/hosts`
echo $be_url
python -m streamlit run app.py

