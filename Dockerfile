# Dockerfile
FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python3 python3-pip curl
RUN pip3 install google-cloud-pubsub googleapis-common-protos==1.5.10 bs4 gspread oauth2client

RUN echo "deb http://packages.cloud.google.com/apt cloud-sdk-xenial main" | \
    tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && apt-get install -y google-cloud-sdk

WORKDIR /app
COPY sheets_util.py worker.py service_keys/metrix_drive_api_service_account_key.json ./
ENV GOOGLE_APPLICATION_CREDENTIALS=metrix_drive_api_service_account_key.json
RUN gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
CMD python3 worker.py
