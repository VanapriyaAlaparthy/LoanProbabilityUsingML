import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
import joblib
from db_config import get_connection

# Load core data from Postgres
conn = get_connection()
df_core = pd.read_sql("SELECT * FROM loan_data", conn)
conn.close()

# Simulate/load external features
extra_features = pd.DataFrame({
    "loan_id": df_core["loan_id"],
    "age": 30 + (df_core.index % 10),
    "has_credit_card": (df_core.index % 2)
})
df = df_core.merge(extra_features, on="loan_id")

# Target & predictors
df['loan_status'] = df['loan_status'].map({'Y': 1, 'N': 0})
y = df['loan_status']
X = df.drop(columns=['loan_id', 'loan_status'])
X = pd.get_dummies(X, dummy_na=True)
X_cols = X.columns

# Train calibrated model for probability
base_model = RandomForestClassifier(n_estimators=200, random_state=42)
model = CalibratedClassifierCV(base_model, method="isotonic", cv=5)
model.fit(X, y)

# Save model & feature columns
joblib.dump((model, list(X_cols)), "model.pkl")
print("✅ Saved calibrated model for app")
