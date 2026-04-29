# backend/services/arvr_map.py
import plotly.express as px
import pandas as pd
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "groundwater_sample.csv")
df = pd.read_csv(DATA_FILE, parse_dates=["date"])

def arvr_map_demo():
    # Minimal demo: uses approximate lat/lon for a few districts
    latlon = {
        "pune": (18.5204, 73.8567),
        "mumbai": (19.0760, 72.8777),
        "bangalore": (12.9716, 77.5946),
        "hyderabad": (17.3850, 78.4867)
    }
    df_sample = df.groupby("district").tail(1)
    df_sample['lat'] = df_sample['district'].str.lower().map(lambda x: latlon.get(x,(0,0))[0])
    df_sample['lon'] = df_sample['district'].str.lower().map(lambda x: latlon.get(x,(0,0))[1])
    fig = px.scatter_mapbox(df_sample, lat='lat', lon='lon', size='level', color='level',
                            hover_name='district', zoom=4, mapbox_style='carto-positron',
                            title='District-level Groundwater (demo)')
    fig.show()


