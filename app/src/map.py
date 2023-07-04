import geopandas as gpd
import streamlit as st
import leafmap.foliumap as leafmap
import json

from src import lang

def MAPPING(gdf, df, feature, municipality, range, language):

    _ = lang.init_translator(language)

    # Add map application
    m = leafmap.Map(minimap_control=False,
                layers_control=False, 
                measure_control=False, 
                attribution_control=False,
                draw_control=False,
                search_control=False)
    
    # Add basemap
    m.add_basemap("CartoDB.PositronNoLabels")

    # Add grey map to visualize NoData for Municipalities out of selected range (only if custom range is selected)
    if range != (0.0, 1.0):
        #gjson = gpd.GeoSeries(gdf.geometry).to_json()
        gjson = gdf.to_json()
        data = json.loads(gjson)
        m.add_geojson(data, layer_name=_("Unselected Municipalities"), style={
            "stroke": True,
            "color": "#808080",
            "weight": 1,
            "opacity": 0.1,
            "fillColor": "#808080",
            "fillOpacity": 0.5,
        })

    # Add choropleth data
    m.add_data(df, 
        column=feature, 
        layer_name=_("CCI Scores"),
        scheme='UserDefined', 
        classification_kwds={'bins': [0.2,0.4,0.6,0.8,1.0]},
        colors=['#DAFBF5', '#A2F6E6', '#6AF0D8', '#34EBC8', '#14CCAA'],
        legend_title= _('Score'),
        legend_kwds={"labels":[_("Major challenges remain"), _("Significant challenges remain"), _("Challenges remain"), _("Minor challenges remain"), _("Challenges achieved")]},
        hover_style={"fillOpacity": 1}
    )

    # Create geodataframe with only geometry --> to mask chosen municipality
    geometry_municipality = gdf[gdf[_('Municipality')].str.contains(municipality)]['geometry']
    boundary_municipality = geometry_municipality.boundary
    gjson = gpd.GeoSeries(boundary_municipality).to_json()
    data = json.loads(gjson)
    m.add_geojson(data, layer_name=_("Selected Municipality"), style={
        "stroke": True,
        "color": "#EA5757",
        "weight": 3,
        "opacity": 1,
        "fillOpacity": 0,
    })

    # Zoom to selected level
    m.fit_bounds(m.get_bounds())
                
    return m