import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, r2_score
from backend.app.engines.data_engine import data_engine

class MLEngine:
    def _clean_currency(self, x):
        if isinstance(x, str):
            clean_str = re.sub(r'[$,%]', '', x)
            try: return float(clean_str)
            except: return x
        return x

    def preprocess_data(self, df):
        df.columns = df.columns.str.strip()
        
        # 1. Clean Objects to Numbers
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].apply(self._clean_currency)
            df_converted = pd.to_numeric(df[col], errors='coerce')
            if df_converted.notna().sum() > 0.5 * len(df):
                df[col] = df_converted

        # 2. Extract Dates
        for col in df.columns:
            if df[col].dtype == 'object':
                try: df[col] = pd.to_datetime(df[col])
                except: pass
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[f"{col}_Year"] = df[col].dt.year
                df[f"{col}_Month"] = df[col].dt.month
                df = df.drop(columns=[col])

        # 3. Fill NAs
        for col in df.select_dtypes(include=np.number).columns:
            df[col] = df[col].fillna(df[col].median())
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].fillna("Unknown").astype(str).str.strip()

        return df

    def train_model(self, dataset_id: str, target_col: str):
        df = data_engine.load_data(dataset_id)
        df.columns = df.columns.str.strip()
        
        # Fuzzy Match Target
        if target_col not in df.columns:
            for col in df.columns:
                if col.lower().strip() == target_col.lower().strip():
                    target_col = col
                    break
        
        if target_col not in df.columns:
            return {"error": f"Column '{target_col}' not found. Available: {list(df.columns)}"}

        df = self.preprocess_data(df)

        # Drop High Cardinality ID cols
        for col in df.columns:
            if df[col].dtype == 'object' and col != target_col:
                if df[col].nunique() > 50:
                    df = df.drop(columns=[col])

        # Determine Task Type BEFORE Encoding (Fixes the nunique bug)
        y_raw = df[target_col]
        is_classification = False
        
        if y_raw.dtype == 'object' or y_raw.nunique() <= 20:
            is_classification = True

        # Encode Features
        for col in df.select_dtypes(include=['object']).columns:
            if col != target_col:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))

        # Split
        X = df.drop(columns=[target_col])
        y = df[target_col]

        # Encode Target if needed
        if y.dtype == 'object':
            le_target = LabelEncoder()
            y = le_target.fit_transform(y.astype(str))

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if is_classification:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            score = accuracy_score(y_test, model.predict(X_test))
            metric = "Accuracy"
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            score = r2_score(y_test, model.predict(X_test))
            metric = "R2 Score"

        importances = model.feature_importances_
        features = X.columns
        feature_imp = sorted(zip(features, importances), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "model_type": "Random Forest Classifier" if is_classification else "Random Forest Regressor",
            "target": target_col,
            "metric": metric,
            "score": round(score * 100, 2),
            "top_features": {k: round(v, 3) for k, v in feature_imp}
        }

ml_engine = MLEngine()
