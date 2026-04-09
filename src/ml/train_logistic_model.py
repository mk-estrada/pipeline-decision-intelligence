
from build_ml_dataset import get_connection, load_ml_dataset

import os
from pathlib import Path

import pandas as pd
import numpy as np
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas


from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score, classification_report

load_dotenv()

def main():

    print("Connecting to Snowflake...")
    conn = get_connection()

    #print("Database:", os.getenv("SNOWFLAKE_DATABASE"))
    #print("Requested schema: ANALYTICS")
    
    df = load_ml_dataset(conn)

    df.columns = df.columns.str.lower()

    #print("Shape:", df.shape)
    #print(df.head())


    feature_cols = [
    "estimated_deal_size_band",
    "regional_office",
    "product_name",
    "deal_age_days"
    ]

    target_col = "won_flag"

    X = df[feature_cols]
    y = df[target_col]
    
    categorical_features = [
    "estimated_deal_size_band",
    "regional_office",
    "product_name"
    ]

    numeric_features = [
        "deal_age_days"
    ]

    print("Starting logistic regression training...")

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical_features),
            ("num", "passthrough", numeric_features)
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("X_train shape:", X_train.shape)
    print("X_test shape:", X_test.shape)
    print("y_train distribution:")
    print(y_train.value_counts(normalize=True))
    print("y_test distribution:")
    print(y_test.value_counts(normalize=True))


    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42))
        ]
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    print("Model training complete.")
    print("First 10 predicted classes:", y_pred[:10])
    print("First 10 predicted probabilities:", y_pred_proba[:10])


    auc = roc_auc_score(y_test, y_pred_proba)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"ROC AUC: {auc:.3f}")
    print(f"Accuracy: {accuracy:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))


    # get feature names from preprocessing
    ohe = model.named_steps["preprocessor"].named_transformers_["cat"]
    cat_feature_names = ohe.get_feature_names_out(categorical_features)

    all_feature_names = np.concatenate([cat_feature_names, numeric_features])

    # get coefficients
    coefficients = model.named_steps["classifier"].coef_[0]

    # combine into dataframe
    coef_df = pd.DataFrame({
        "feature": all_feature_names,
        "coefficient": coefficients
    })

    coef_df = coef_df.sort_values(by="coefficient", ascending=False)

    print(coef_df)

    conn.close()

if __name__ == "__main__":
    main()