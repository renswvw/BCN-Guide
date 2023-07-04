import streamlit as st

from src import lang
from src.map import MAPPING


# If-else statement to enable weight change only if 'CCI' is selected.
def WEIGHT(gdf, feature, municipality, language):

    _ = lang.init_translator(language)

    if feature == 'CCI':
        # NUMBER INPUT FUNCTION
        # Create number input boxes to change weights
        col1, col2, col3, col4 = st.columns(4)

        with col1: 
            new_weight_D = st.number_input(
                label = _("Digitalization"),
                min_value = 0.0,
                max_value = 1.0,
                value = 0.2,)
        with col2: 
            new_weight_ECR = st.number_input(
                label = _("Energy & Climate"),
                min_value = 0.0,
                max_value = 1.0, # - new_weight_D,
                value = 0.3) # - (new_weight_D - 0.2),) 
        with col3: 
            new_weight_M = st.number_input(
                label = _("Mobility"),
                min_value = 0.0,
                max_value = 1.0, # - new_weight_D - new_weight_ECR,
                value = 0.2) #- (new_weight_ECR - 0.3),) 
        with col4: 
            new_weight_W = st.number_input(
                label = _("Waste"),
                min_value = 0.0,
                max_value = 1.0, # - new_weight_D - new_weight_ECR - new_weight_M,
                value = 0.3) # - (new_weight_M - 0.2),)
                #disabled = True)

        # Calculate sum of total new weights
        total_weights = new_weight_D + new_weight_ECR + new_weight_M + new_weight_W

        # If-else statement to ensure that weights sum up to 1.0
        if total_weights == 1.0:
            # Calculate CCI with new weights
            gdf['New_CCI'] = gdf[_('Digitalization')] * new_weight_D + gdf[_('Energy_Climate_Resources')] * new_weight_ECR + gdf[_('Mobility')] * new_weight_M + gdf[_('Waste')] * new_weight_W 
            
            # Map new weights --> use defined function
            map = MAPPING(
                gdf,
                gdf, 
                'New_CCI',
                municipality,
                (0.0, 1.0),
                language)
            
            map.to_streamlit(height=525, use_container_width=True) 
            
        else:
            # Print warning message
            st.warning(_('Sum of weights is not equal 1.0.'), icon="⚠️")

            # Map old weights --> use defined function
            map = MAPPING(
                gdf,
                gdf, 
                'CCI',
                municipality,
                (0.0, 1.0),
                language)
            
            map.to_streamlit(height=525, use_container_width=True) 
    
    # If feature 'CCI' is not selected, do not print weight adjustment
    else:
        # Map selected feature without option to change weight
        map = MAPPING(
                gdf,
                gdf, 
                feature,
                municipality,
                (0.0, 1.0),
                language)
        
        map.to_streamlit(height=575, use_container_width=True)