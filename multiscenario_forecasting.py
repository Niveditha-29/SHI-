import pandas as pd
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "groundwater_sample.csv")
df = pd.read_csv(DATA_FILE, parse_dates=["date"])

def forecast_groundwater(district: str):
    d = district.lower()
    df_d = df[df['district'].str.lower()==d].sort_values('date')
    if df_d.empty:
        return None
    last_level = df_d['level'].iloc[-1]
    # Very simple scenario model: small percent changes
    best = round(last_level * 1.02, 2)
    avg = round(last_level, 2)
    worst = round(last_level * 0.95, 2)
    return {"district": district.title(), "best_case": best, "average_case": avg, "worst_case": worst}


