import pandas as pd
import numpy as np
from backend.app.engines.data_engine import data_engine

class EDAEngine:
    def generate_summary(self, dataset_id: str) -> dict:
        df = data_engine.load_data(dataset_id)

        # 1. Clean Data (Force numeric)
        for col in df.columns:
            df_converted = pd.to_numeric(df[col], errors='coerce')
            if df_converted.notna().sum() > 0:
                df[col] = df_converted

        # 2. Create the Summary
        summary = {
            "dataset_id": dataset_id,
            "rows": int(df.shape[0]),
            "cols": int(df.shape[1]),
            "column_names": list(df.columns),
            "data_types": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "preview": df.head(5).replace({np.nan: None}).to_dict(orient="records")
        }
        
        # 3. Numeric Stats
        try:
            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                summary["numeric_stats"] = numeric_df.describe().replace({np.nan: None}).to_dict()
                
                # --- THE FIX: ADD SAMPLE DATA FOR PLOTTING ---
                # We take 50 random rows so the AI has enough points to make a chart look real
                # orient='list' makes it easy for AI to grab arrays: { "Age": [10, 20...], "Fare": [5, 15...] }
                sample_size = min(50, len(df))
                plot_sample = numeric_df.sample(sample_size).replace({np.nan: None})
                summary["chart_data"] = plot_sample.to_dict(orient="list")

        except Exception as e:
            summary["numeric_stats_error"] = str(e)
            
        return summary

eda_engine = EDAEngine()
