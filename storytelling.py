import pandas as pd
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "groundwater_sample.csv")
df = pd.read_csv(DATA_FILE, parse_dates=["date"])

def generate_story(district: str, lang="en"):
    d = district.lower()
    df_d = df[df['district'].str.lower()==d].sort_values('date')
    if df_d.empty:
        return "No data available." if lang=="en" else "डेटा उपलब्ध नहीं है।"
    start = df_d['level'].iloc[0]
    end = df_d['level'].iloc[-1]
    diff = round(end - start, 2)
    if lang=="hi":
        trend = "बढ़ रहा है" if diff>0 else "घट रहा है" if diff<0 else "स्थिर है"
        return f"{district.title()} में पिछले {len(df_d)} रिकॉर्ड में भूजल स्तर {trend} (शुरुआत: {start}m, अब: {end}m, परिवर्तन: {diff}m)।"
    trend = "increasing" if diff>0 else "decreasing" if diff<0 else "stable"
    return f"In {district.title()}, groundwater over {len(df_d)} records is {trend} (start: {start}m, now: {end}m, change: {diff}m)."

