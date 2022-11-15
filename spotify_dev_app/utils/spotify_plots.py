import numpy as np
import pandas as pd
import plotly.graph_objects as go
from colormap import rgb2hex


def createRadarChart(df: pd.DataFrame, attributes, user: str, color='blue') -> go.Figure:
    df = df.loc[user][attributes]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=df.values,
        theta=df.index.values,
        fill='toself'
    )
    )
    # update colors
    fig.update_traces(fillcolor=rgb2hex(
        color[0], color[1], color[2]), line_color=rgb2hex(color[0], color[1], color[2]))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=False
    )
    #fig.update_layout(
    #    title={
    #        'text': f"<br>{user}</br> addition to the playlist",
    #        'y': 0.9,
    #        'x': 0.5,
    #        'xanchor': 'center',
    #        'yanchor': 'top'})
    return fig
