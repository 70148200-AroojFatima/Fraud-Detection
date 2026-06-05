import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report
)
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("fraud-detection-experiment")

print("Loading real credit card fraud dataset...")
df = pd.read_csv("data/creditcard.csv")
print(f"Dataset shape: {df.shape}")
print(f"Fraud transactions: {df['Class'].sum()} ({df['Class'].mean()*100:.3f}%)")

df['Amount_scaled'] = StandardScaler().fit_transform(df[['Amount']])
df['Time_scaled'] = StandardScaler().fit_transform(df[['Time']])
df.drop(['Amount', 'Time'], axis=1, inplace=True)

X = df.drop('Class', axis=1)
y = df['Class']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train size: {X_train.shape}, Test size: {X_test.shape}")

print("Applying SMOTE to handle class imbalance...")
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
print(f"After SMOTE - Train size: {X_train_res.shape}")

with mlflow.start_run(run_name="RandomForest_FraudDetection"):

    n_estimators = 100
    max_depth = 20
    min_samples_split = 5
    random_state = 42

    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("min_samples_split", min_samples_split)
    mlflow.log_param("random_state", random_state)
    mlflow.log_param("dataset", "Kaggle Credit Card Fraud 2013 (ULB MLG)")
    mlflow.log_param("dataset_rows", len(df))
    mlflow.log_param("smote_applied", True)

    print("Training Random Forest model...")
    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=random_state,
        n_jobs=-1
    )
    clf.fit(X_train_res, y_train_res)

    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec  = recall_score(y_test, y_pred)
    f1   = f1_score(y_test, y_pred)
    auc  = roc_auc_score(y_test, y_prob)

    print(f"\nAccuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"ROC-AUC:   {auc:.4f}")
    print("\n", classification_report(y_test, y_pred, target_names=["Legitimate", "Fraud"]))

    mlflow.log_metric("accuracy",  acc)
    mlflow.log_metric("precision", prec)
    mlflow.log_metric("recall",    rec)
    mlflow.log_metric("f1_score",  f1)
    mlflow.log_metric("roc_auc",   auc)

    mlflow.sklearn.log_model(
        clf,
        artifact_path="random-forest-fraud",
        registered_model_name="FraudDetectionModel"
    )

    os.makedirs("model", exist_ok=True)
    joblib.dump(clf, "model/model.pkl")
    print("\nModel saved to model/model.pkl")
    print("MLflow run complete. Run ID:", mlflow.active_run().info.run_id)
