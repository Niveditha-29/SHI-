import pandas as pd
import plotly.express as px
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "groundwater_sample.csv")
df = pd.read_csv(DATA_FILE, parse_dates=["date"])

# generate and save HTML chart to backend/data/charts/
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "backend_charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

def generate_trend_chart(districts, lang="en"):
    if isinstance(districts, str):
        districts = [districts]
    df_cmp = df[df['district'].str.lower().isin([d.lower() for d in districts])]
    if df_cmp.empty:
        return None
    fig = px.line(df_cmp, x='date', y='level', color='district',
                  title=("Groundwater Trend" if lang=="en" else "भूजल प्रवृत्ति"),
                  labels={"date": "Date" if lang=="en" else "दिनांक",
                          "level": "Level (m)" if lang=="en" else "स्तर (m)",
                          "district": "District" if lang=="en" else "जिला"})
    filename = "_".join([d.title() for d in districts]) + ".html"
    out = os.path.join(CHARTS_DIR, filename)
    fig.write_html(out)
    return out
