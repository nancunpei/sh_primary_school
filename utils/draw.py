import pandas as pd

import plotly.graph_objects as go

from config.config import LOCATION_CSV


def draw_location():
    df = pd.read_csv(LOCATION_CSV, delim_whitespace=True)
    address_list = df['address'].to_list()
    lat_list = df['lat'].to_list()
    lon_list = df['lon'].to_list()
    tier_list = df['tier'].to_list()

    mapbox_access_token = 'pk.eyJ1Ijoia29wZWkiLCJhIjoiY2tkaDFwOTdlMXdobTJwbXBhd2tlYzYyNiJ9.dwMoIYpHrHgrGTCSrGnHSA'
    fig = go.Figure(go.Scattermapbox(
        lat=lat_list,
        lon=lon_list,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14
        ),
        text=address_list
    ))

    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=31,
                lon=121
            ),
            pitch=0,
            zoom=20
        )
    )

    return fig