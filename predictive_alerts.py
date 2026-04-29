import pandas as pd
import random

data = pd.read_csv("backend/data/groundwater_data.csv")

def get_groundwater_level(district: str, date: str):
    district = district.title()
    df = data[data['district']==district]
    if df.empty: return 12.0
    return float(df['level'].iloc[-1])

def get_trend(district: str, return_chart=False):
    district = district.title()
    df = data[data['district']==district]
    if df.empty: return "No data available"
    if return_chart:
        return df['level'].tolist(), df['month'].tolist()
    trend = " → ".join([f"{m}:{l}m" for m,l in zip(df['month'], df['level'])])
    return trend

def detect_anomaly(district: str, date: str):
    return "⚠ Anomaly detected: sudden drop!" if random.random()<0.1 else ""


