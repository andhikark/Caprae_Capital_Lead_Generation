import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
import joblib
import os

def train_lead_score_model(data_path="data/training_set.csv", model_path="models/lead_model.pkl"):
    os.makedirs("models", exist_ok=True)
    df = pd.read_csv(data_path)

    df["has_email"] = df["email"].notnull().astype(int)
    df["has_linkedin"] = df["linkedin"].notnull().astype(int)
    def parse_employees(e):
        try:
            if "-" in e:
                low, high = map(int, e.split("-"))
                return (low + high) // 2
            return int(e)
        except:
            return 0

    df["employees"] = df["employees"].astype(str).apply(parse_employees)

    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    industry_encoded = ohe.fit_transform(df[["industry"]])
    industry_df = pd.DataFrame(industry_encoded, columns=ohe.get_feature_names_out(["industry"]))

    X = pd.concat([
        df[["employees", "has_email", "has_linkedin"]].fillna(0),
        industry_df
    ], axis=1)
    y = df["score"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    print(f"✅ Model trained. MSE: {mse:.2f}")
    joblib.dump(model, model_path)
    joblib.dump(ohe, "models/industry_encoder.pkl")

def predict_lead_scores(df, model_path="models/lead_model.pkl", encoder_path="models/industry_encoder.pkl"):
    if not os.path.exists(model_path) or not os.path.exists(encoder_path):
        raise FileNotFoundError("Model or encoder not found. Please train the model first.")

    model = joblib.load(model_path)
    ohe = joblib.load(encoder_path)

    df = df.copy()
    df["has_email"] = df["email"].notnull().astype(int)
    df["has_linkedin"] = df["linkedin"].notnull().astype(int)

    def parse_employees(e):
        try:
            if "-" in e:
                low, high = map(int, str(e).split("-"))
                return (low + high) // 2
            return int(e)
        except:
            return 0

    df["employees"] = df["employees"].astype(str).apply(parse_employees)
    industry_encoded = ohe.transform(df[["industry"]])
    industry_df = pd.DataFrame(industry_encoded, columns=ohe.get_feature_names_out(["industry"]))

    X = pd.concat([
        df[["employees", "has_email", "has_linkedin"]].fillna(0).reset_index(drop=True),
        industry_df.reset_index(drop=True)
    ], axis=1)

    df["predicted_score"] = model.predict(X).astype(int)
    return df

if __name__ == "__main__":
    train_lead_score_model()
