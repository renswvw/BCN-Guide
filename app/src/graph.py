import streamlit as st
import geopandas as pd
import plotly.graph_objects as go
import plotly.express as px

from src.gui import GRAPH_TITLE
from src import lang

# SPEEDOMETER / GAUGE PLOT
# Define direction of delta
def GAUGE_DELTA(gdf, df, feature):
    feature_value = df[feature].iloc[0]
    feature_mean = gdf[feature].mean()
    if feature_value < feature_mean:
        direction = 'decreasing'
    else:
        direction = 'increasing'
    return direction

# Define color of delta
def GAUGE_COLOR(gdf, df, feature):
    feature_value = df[feature].iloc[0]
    feature_mean = gdf[feature].mean()
    if feature_value < feature_mean:
        color = '#DAFBF5'
    elif feature_value == feature_mean:
        color = '#240115'
    else:
        color = '#14CCAA'
    return color

# Plot Gauge figure
def GAUGE_FIG(gdf, df, feature, direction, color, language):

    _ = lang.init_translator(language)

    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = df[feature].iloc[0],
        #number={'font': {"size": 60}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': GRAPH_TITLE(_("CCI Score"))},
        delta = {'reference': gdf[feature].mean(), direction: {'color': color}},
        gauge = {
            'axis': {'range': [None, 1], 'tickwidth': 1, 'tickcolor': "#FFFFFF"},
            'bar': {'color': "rgba(0,0,0,0.0)"},
            'bgcolor': "rgba(0,0,0,0.0)",
            'borderwidth': 0,
            'steps': [ 
                {'range': [0, 0.2], 'color': '#DAFBF5'},
                {'range': [0.2, 0.4], 'color': '#A2F6E6'}, 
                {'range': [0.4, 0.6], 'color': '#6AF0D8'}, 
                {'range': [0.6, 0.8], 'color': '#34EBC8'}, 
                {'range': [0.8, 1.0], 'color': '#14CCAA'}], 
            'threshold': {
                'line': {'color': "#EA5757", 'width': 4},
                'thickness': 0.8,
                'value': df[feature].iloc[0]}}))

    fig.update_layout(height=200, paper_bgcolor = "rgba(0,0,0,0.0)", font = {'color': "#FFFFFF"}, margin=dict(l=30, r=15, t=20, b=10))
    return fig


def BAR_CHART(df, language):

    import plotly.io as pio

    _ = lang.init_translator(language)

    # BAR CHART
    # Plot Bars for sub-levels CCI
    fig = px.bar(
        df.T, 
        y=df.T.iloc[2:,0], 
        x=[_("Digitalization"), _("Energy_Climate_Resources"), _("Mobility"), _("Waste")], 
        title=GRAPH_TITLE(_("CCI Categories")),    
        color_discrete_sequence=['#3CECCA']
    )

    # Update the layout
    fig.update_layout(
        height=255,
        xaxis=dict(
            title=None,
            tickfont=dict(size=12),
            tickangle=0,
            tickmode='array',
            tickvals=[0, 1, 2, 3],
            ticktext=[_("Dig"), _("Ene"), _("Mob"), _("Was")],
            tickwidth=1,
            tickcolor='#FFFFFF',
            showline=False,
            linewidth=2,
            linecolor='#FFFFFF',
            mirror=True,
            ticks="outside"
        ),
        yaxis=dict(
            title=None,
            showgrid=True,  
            gridwidth=1,   
            gridcolor='#FFFFFF', 
            tickmode='array',
            tickvals=[0.0, 0.5, 1.0], 
            rangemode='nonnegative'  
        ),
        shapes=[  
            dict(
                type='line',
                xref='paper',
                x0=0.0,
                y0=1.0,
                x1=1.0,
                y1=1.0,
                line=dict(color='white', width=1)
            )
        ],
        margin=dict(l=10, r=10, t=30, b=10, pad=0),
        font=dict(color="#FFFFFF"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    # Set grid colors to white
    fig.update_yaxes(zeroline=True, zerolinecolor="#FFFFFF", showgrid=True, gridcolor="#FFFFFF")
        
    # Set color for label of hovered bar
    custom_labels = [_("Digitalization"), _("Energy & Climate"), _("Mobility"), _("Waste")]

    fig.update_traces(selector=dict(type="bar"), 
        hovertemplate="<b>%{x: custom_labels}</b><br>%{y:.2f}", # Change here the labels of the hovers
        hoverlabel=dict(bgcolor="#EA5757"),
        customdata=custom_labels)
    
    return fig