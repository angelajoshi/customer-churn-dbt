import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
import pickle

def train_model(data_path="data/churn_features.csv"):
    # Placeholder for actual data loading and preprocessing
    # In a real scenario, this would load from PostgreSQL via dbt output
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}. Please ensure data is generated.")
        return

    X = df.drop('churn_label', axis=1) # Assuming 'churn_label' is the target
    y = df['churn_label']

    # Simple feature selection for placeholder
    # In a real scenario, features would be more carefully selected/engineered
    if 'customer_id' in X.columns:
        X = X.drop('customer_id', axis=1)
    if 'gender' in X.columns:
        X = pd.get_dummies(X, columns=['gender'], drop_first=True)
    if 'contract_type' in X.columns:
        X = pd.get_dummies(X, columns=['contract_type'], drop_first=True)
    if 'last_payment_date' in X.columns:
        X = X.drop('last_payment_date', axis=1) # Drop date for simplicity

    # Fill any remaining NaNs for demonstration
    X = X.fillna(X.mean())

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    model.fit(X_train_scaled, y_train)

    # Save model and scaler
    with open('ml/churn_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('ml/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    print("Model and scaler trained and saved.")

if __name__ == "__main__":
    # This script expects a 'churn_features.csv' in the data directory for standalone testing.
    # In the full pipeline, dbt would output to a database, and Prefect would orchestrate.
    train_model(data_path="../data/churn_features.csv")
