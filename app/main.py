from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os
from prometheus_fastapi_instrumentator import Instrumentator

MODEL_PATH = os.getenv("MODEL_PATH", "model/model.pkl")
try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded from {MODEL_PATH}")
except Exception as e:
    raise RuntimeError(f"Could not load model: {e}")

app = FastAPI(
    title="Real-Time Fraud Detection API",
    description="Detects fraudulent financial transactions using Random Forest. Student: Arooj Fatima | SAP: 70148200",
    version="1.0.0"
)

Instrumentator().instrument(app).expose(app)

class Transaction(BaseModel):
    V1: float; V2: float; V3: float; V4: float; V5: float
    V6: float; V7: float; V8: float; V9: float; V10: float
    V11: float; V12: float; V13: float; V14: float; V15: float
    V16: float; V17: float; V18: float; V19: float; V20: float
    V21: float; V22: float; V23: float; V24: float; V25: float
    V26: float; V27: float; V28: float
    Amount_scaled: float
    Time_scaled: float

@app.get("/")
def root():
    return {
        "message": "Real-Time Fraud Detection API",
        "student": "Arooj Fatima",
        "sap_id": "70148200",
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict")
def predict(transaction: Transaction):
    try:
        features = np.array([[
            transaction.V1, transaction.V2, transaction.V3, transaction.V4,
            transaction.V5, transaction.V6, transaction.V7, transaction.V8,
            transaction.V9, transaction.V10, transaction.V11, transaction.V12,
            transaction.V13, transaction.V14, transaction.V15, transaction.V16,
            transaction.V17, transaction.V18, transaction.V19, transaction.V20,
            transaction.V21, transaction.V22, transaction.V23, transaction.V24,
            transaction.V25, transaction.V26, transaction.V27, transaction.V28,
            transaction.Amount_scaled, transaction.Time_scaled
        ]])
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0].tolist()
        result = "Fraudulent" if prediction == 1 else "Legitimate"
        return {
            "prediction": int(prediction),
            "result": result,
            "fraud_probability": round(probability[1], 4),
            "legitimate_probability": round(probability[0], 4)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
