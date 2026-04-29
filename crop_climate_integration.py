import pandas as pd
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "groundwater_sample.csv")
df = pd.read_csv(DATA_FILE, parse_dates=["date"])

crop_water_usage = {
    "wheat": 1.2,
    "rice": 1.5,
    "maize": 1.1,
    "sugarcane": 1.8
}

def crop_recommendation(district: str, crop: str):
    d = district.lower()
    df_d = df[df['district'].str.lower()==d]
    if df_d.empty:
        return f"No data for {district.title()}."
    latest = df_d['level'].iloc[-1]
    need = crop_water_usage.get(crop.lower(), 1.0)
    if latest - need < 2:
        return f"Caution: {crop.title()} may stress groundwater in {district.title()}. Consider alternatives."
    return f"{crop.title()} suitable in {district.title()} for this season."


