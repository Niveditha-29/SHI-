import pandas as pd
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "groundwater_sample.csv")
df = pd.read_csv(DATA_FILE, parse_dates=["date"])

def generate_recommendation(district: str, lang="en"):
    d = district.lower()
    df_d = df[df['district'].str.lower()==d]
    if df_d.empty:
        return "No recommendation data." if lang=="en" else "सुझाव के लिए डेटा उपलब्ध नहीं।"
    latest = df_d.sort_values('date').iloc[-1]['level']
    tips = []
    if latest < 10:
        tips.append("Use drip irrigation")
        tips.append("Reduce borewell extraction")
    elif latest < 12:
        tips.append("Conserve water and monitor levels")
    else:
        tips.append("Normal usage; continue monitoring")
    if lang=="hi":
        # basic translations
        trans = {"Use drip irrigation":"ड्रिप सिंचाई का उपयोग करें",
                 "Reduce borewell extraction":"बोरवेल निष्कर्षण कम करें",
                 "Conserve water and monitor levels":"पानी बचाएं और स्तर की निगरानी करें",
                 "Normal usage; continue monitoring":"सामान्य उपयोग; निगरानी जारी रखें"}
        return [trans.get(t,t) for t in tips]
    return tips
