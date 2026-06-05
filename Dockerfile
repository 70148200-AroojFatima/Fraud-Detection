FROM python:3.11-slim

LABEL maintainer="Arooj Fatima"
LABEL sap_id="70148200"
LABEL description="Real-Time Fraud Detection MLOps System"

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY app/main.py .
COPY model/model.pkl ./model/model.pkl

EXPOSE 8000

ENV MODEL_PATH=model/model.pkl

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
