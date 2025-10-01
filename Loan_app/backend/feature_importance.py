import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from db_config import get_connection

# Load core data
conn = get_connection()
df_core = pd.read_sql("SELECT * FROM loan_data", conn)
conn.close()

# Extra features
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

# Train regular Random Forest for feature importance
rf_model = RandomForestClassifier(n_estimators=200, random_state=42)
rf_model.fit(X, y)

# Compute feature importance
importances = rf_model.feature_importances_
feat_importance_df = pd.DataFrame({
    "feature": X_cols,
    "importance": importances
}).sort_values(by="importance", ascending=False)

# Save to CSV
feat_importance_df.to_csv("feature_importance.csv", index=False)
print("✅ Feature importance saved to feature_importance.csv")
print(feat_importance_df.head(10))  # Top 10 features
