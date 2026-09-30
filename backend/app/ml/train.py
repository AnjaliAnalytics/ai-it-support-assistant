import os
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Synthetic Dataset Generation
def generate_synthetic_data(num_samples: int = 500) -> pd.DataFrame:
    np.random.seed(42)
    categories = ["Network", "Software", "Hardware", "Database", "Authentication", "Access"]
    criticalities = ["Low", "Medium", "High", "Critical"]
    
    descriptions = [
        "Entire Mumbai office internet outage. Network router down.",
        "Cannot reset password on identity portal.",
        "Laptop screen flickering intermittently.",
        "Production database server high memory usage and query timeout.",
        "Outlook desktop application closing unexpectedly.",
        "VPN disconnects every 10 minutes when connected remotely.",
        "Citrix server host unreachable for finance department.",
        "Printer in floor 3 out of paper.",
        "Access request to marketing share drive.",
        "Core payroll database offline during end-of-month run."
    ]

    data = []
    for _ in range(num_samples):
        idx = np.random.randint(0, len(descriptions))
        desc = descriptions[idx]
        cat = categories[np.random.randint(0, len(categories))]
        crit = criticalities[np.random.randint(0, len(criticalities))]
        users = np.random.randint(1, 500)
        desc_len = len(desc)

        # Rule-based priority assignment for training labels
        if "outage" in desc.lower() or "offline" in desc.lower() or users > 250 or crit == "Critical":
            priority = "P1"
        elif "timeout" in desc.lower() or "disconnects" in desc.lower() or users > 100 or crit == "High":
            priority = "P2"
        elif "password" in desc.lower() or "application" in desc.lower() or users > 20:
            priority = "P3"
        else:
            priority = "P4"

        data.append({
            "description": desc,
            "category": cat,
            "system_criticality": crit,
            "affected_users": users,
            "description_length": desc_len,
            "priority": priority
        })

    return pd.DataFrame(data)


def train_model():
    print("Generating synthetic dataset...")
    df = generate_synthetic_data(1000)

    X = df[["description", "category", "system_criticality", "affected_users", "description_length"]]
    y = df["priority"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Feature Processing Pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ("text", TfidfVectorizer(max_features=100, stop_words="english"), "description"),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["category", "system_criticality"]),
            ("num", StandardScaler(), ["affected_users", "description_length"])
        ]
    )

    # Simple, Interpretable Model: Logistic Regression
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=500, random_state=42))
        ]
    )

    print("Training Logistic Regression pipeline...")
    pipeline.fit(X_train, y_train)

    # Evaluation
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")

    print("\n--- MODEL EVALUATION METRICS ---")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Weighted F1 Score: {f1:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    # Save Artifacts
    artifacts_dir = os.path.join("backend", "app", "ml", "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)
    model_path = os.path.join(artifacts_dir, "priority_model.joblib")
    
    joblib.dump(pipeline, model_path)
    print(f"\nModel artifact successfully saved to: {model_path}")


if __name__ == "__main__":
    train_model()