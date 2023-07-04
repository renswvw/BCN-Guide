import geopandas as gpd
import streamlit as st
import leafmap.foliumap as leafmap

from src import lang
from src.gui import GUI_STYLE, TITLE, INTRODUCTION
from src.map import MAPPING
from src.graph import GAUGE_DELTA, GAUGE_COLOR, GAUGE_FIG, BAR_CHART
from src.weight import WEIGHT
from src.__version__ import version

# Set Data Source
URL_GEO = "https://github.com/renswvw/CircularCityIndexSpain/raw/main/data/processed/CCI/03_index/streamlit_files/CCI_Index_simplify_small.gpkg?raw=true"

# Set Defaults
DEFAULT_OPTION_LEVEL = "Extremadura"
DEFAULT_OPTION_MUNICIPALITY = "Mérida" # or "" --> empty
DEFAULT_OPTION_FEATURE = "CCI"
DEFAULT_LANGUAGE = "en"

# Set layout of page
st.set_page_config(
    page_title="Circular City Index - Spain",
    page_icon="	:recycle:",
    layout="wide",
    menu_items={
        "Get Help": "https://www.bsc.es/viz",
        "Report a bug": "https://www.bsc.es/viz",
        "About": (
            "[Data Analytics and Visualization Team](https://bsc.es/viz),"
            "[Barcelona Supercomputing Center](https://bsc.es), BSC."
        ),
    },
)

# Set HTML Style for UI/UX of page
GUI_STYLE()

# Define language of page
language = st.radio(
        "",
        lang.language_from_code.keys(),
        index=list(lang.language_from_code.keys()).index(DEFAULT_LANGUAGE),
        format_func=lambda code: lang.language_from_code[code],
        horizontal=True,
    )
_ = lang.init_translator(language)

# Dictionary of Autonomous Communities
AREA_TO_PREDICT_dict = {_("Andalusia"): "01", _("Aragon"): "02", _("Asturias"): "03", _("Balearic Islands"): "04", _("Canary Islands"): "05", _("Cantabria"): "06", _("Castile and León"): "07", _("Castilla-La Mancha"): "08", _("Catalonia"): "09", _("Valencia"): "10", _("Extremadura"): "11", _("Galicia"): "12", _("Madrid"): "13", _("Murcia"): "14", _("Navarre"): "15", _("Basque Country"): "16", _("La Rioja"): "17", _("Ceuta"): "18", _("Melilla"): "19", _("Minor Plazas de Soberanía"): "20"}

# Data to cache
@st.cache_data
def get_data(url_geo: str):
    gdf = gpd.read_file(URL_GEO)
    return gdf
gdf = get_data(url_geo=URL_GEO)

# Translate columns of geodataframe
gdf.rename(columns={
    'Municipality': _("Municipality"),
    'Digitalization': _('Digitalization'), 
    'Energy_Climate_Resources': _('Energy_Climate_Resources'),
    'Mobility': _('Mobility'), 
    'Waste': _('Waste')},
    inplace=True)

# Set tabs
main_tab, side_tab = st.tabs([_("Municipality Dashboard"), _("Research Dashboard")])

# First tab - Municipality Dashboard
with main_tab:
    col1, col2 = st.columns((3,1))

    with col1:
        # Title + text
        TITLE(_("Circular City Index Dashboard"))
        INTRODUCTION(_("This dashboard is developed to show the Circular City Index applied on Spain, and empowers policymakers with data-driven insights across key indicators. The index supports driving targeted strategies for sustainable urban development, fostering circularity and spearheading Spain's green transition."))

    with col2:
        EMPTY = 0

    # Data Selection
    # Create columns for select boxes
    col1, col2, col3, col4 = st.columns(4)

    with col1: 
        # Function to obtain Autonomous Community (AUC) code for a chosen municipality (MUN)
        level_list = [_("Spain"), _("Iberian Pensinula")] + sorted(list(AREA_TO_PREDICT_dict.keys()))
        
        # selectbox to select options for study level
        option_level = st.selectbox(
            _("Select Autonomous Community"),
            level_list,
            index=level_list.index(DEFAULT_OPTION_LEVEL)
            )        

        # Filter dataset to selected study area
        if option_level in AREA_TO_PREDICT_dict:
            gdf = gdf[gdf["CTOT"].str.contains(r'^' + AREA_TO_PREDICT_dict[option_level])]
        elif option_level == _("Iberian Pensinula"):
            gdf = gdf[~gdf.CTOT.str.contains(r'^04|^05|^18|^19|^20')] 
        elif option_level == _("Spain"):
            pass

    with col2:
        # Function to obtain Autonomous Community (AUC) code for a chosen municipality (MUN)
        municipality_list = sorted(list(gdf[_('Municipality')].unique()))
        
        # selectbox to select options for study level    
        option_municipality = st.selectbox(
            _("Select Municipality"),
            municipality_list,
            index=municipality_list.index(municipality_list[0]),
        )    
    
    with col3:
        # create a slider to hold CCI scores
        option_range = st.slider(
            label=_("Select Range of Score"),
            min_value=0.0,
            max_value=1.0,
            value=(0.0, 1.0),
            key="score_slider"
        )

        # Finalize dataframe by setting CTOT as index, dropping other columns, and rounding to 3 decimals.
        gdf.set_index("CTOT", inplace=True)
        gdf = gdf.round(decimals=3)
        df = gdf.drop(gdf.columns[-1:], axis=1)

        #Configure and filter the slider widget for interactivity
        range_score = gdf[(gdf[DEFAULT_OPTION_FEATURE].between(*option_range))]

    with col4:
        #EMPTY
        EMPTY = 0

    # Create columns for dashboard
    col1, col2 = st.columns((3,1))
    
    with col1:
        # Map  
        map = MAPPING(
            gdf=gdf,
            df=range_score, 
            feature=DEFAULT_OPTION_FEATURE,
            municipality=option_municipality,
            range=option_range,
            language=language)
        
        map.to_streamlit(height=525, use_container_width=True) 

        # Write additional information
        st.markdown(_("[Data Analytics and Visualization Team](https://bsc.es/viz/team/), [Barcelona Supercomputing Center](https://bsc.es/) (BSC). [circular-city-index-viewer](https://github.com/BSCCNS/circular-city-index-viewer.git)"))

    with col2:
        # Filter the dataframe based on the search term
        selected_municipality_df = df[df[_("Municipality")].str.match(f"^{option_municipality}$", case=False)]

        # SPEEDOMETER / GAUGE PLOT
        # Plot index outcome
        fig_gauge = GAUGE_FIG(
            gdf=gdf,
            df=selected_municipality_df, 
            feature=DEFAULT_OPTION_FEATURE,
            direction=GAUGE_DELTA(gdf, selected_municipality_df, DEFAULT_OPTION_FEATURE), 
            color=GAUGE_COLOR(gdf, selected_municipality_df, DEFAULT_OPTION_FEATURE),
            language=language,
            )
        
        st.plotly_chart(fig_gauge, height=200, use_container_width=True) 

        # BAR CHART
        # Plot Bars for sub-levels CCI    
        fig_bar_chart = BAR_CHART(
            df=selected_municipality_df,
            language=language) 
        
        st.plotly_chart(fig_bar_chart, height=250, use_container_width=True)

# Second tab - Research Dashboard
with side_tab:
    TITLE(_("Map of ") + option_level + _(" - Change Weights"))

    # Feature  list
    feature = df.iloc[: , 1:] 
    features = feature.columns.values

    # selectbox to select options for features
    option_feature = st.selectbox(
        _("Select Feature"),
        features,
        index=features.tolist().index(DEFAULT_OPTION_FEATURE),
    )

    # Plot Map and Weights
    WEIGHT(
        gdf=gdf, 
        feature=option_feature, 
        municipality=option_municipality,
        language=language)
    
    # credits and version
    st.markdown(_("Supported by SoBigData++ ([Gr. N. 871042](https://cordis.europa.eu/project/id/871042))."))