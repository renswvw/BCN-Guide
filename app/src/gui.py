import streamlit as st

# Define layout of page
def GUI_STYLE():
    gui_app = """
        <style>
            /* define font style */
            @import url('https://fonts.googleapis.com/css?family=Roboto');

            html, body, [class*="streamlit"]  {
                font-family: "Roboto", sans-serif;
                font-weight: normal;
                letter-spacing: 0px;
                color: #FFFFFF;
                text-align: left;
            }
            /* color text - selectbox */
            .st-ax {
                color: #EA5757;
            }
            /* color icon and text list - selectbox*/
            .st-co, .st-bs, .st-cz {
                color: #EA5757;
            }
            /* color borders - selectbox */
            .st-by, .st-de, .st-dw {
                border-bottom-color: #3CECCA;
            }
            .st-bx, .st-df, .st-dw {
                border-top-color: #3CECCA;
            }
            .st-bw, .st-dg, .st-dw {
                border-right-color: #3CECCA;
            }
            .st-bv, .st-dh, .st-dw {
                border-left-color: #3CECCA;
            }
            /* color button - number input box */
            .css-2q0qfv {
                color: #EA5757;
            }
            /* color borders and text - number input box */
            .css-vxbo1p {
                border-color: #3CECCA;
                color: #EA5757;
            }
        </style>
        """
    st.markdown(gui_app, unsafe_allow_html=True) 
 
# Define function for title and layout
def TITLE(text):
    title = st.markdown(
        f"""    
        <h1 style='
            text-align: left;
            font: normal normal medium 36px/42px Roboto;
            letter-spacing: 0px;
            margin-top: 0px;
            margin-bottom: 0px;
            color: #34EBC8;
            opacity: 1;
        '>
            {text}
        </h1>
        """,
        unsafe_allow_html=True
        )
    return title

# Define function for introduction text and layout
def INTRODUCTION(text):
    introduction = st.write(
        f"""
        <h2 style='
            text-align: justify;
            font: normal normal normal 18px/22px Roboto;
            letter-spacing: 0px;
            margin-bottom: 10px;
            color: #FFFFFF;
            opacity: 1;
        '>
            {text}
        </h2>
        """,
        unsafe_allow_html=True,
        )
    return introduction
    
# Define titles of graphs
def GRAPH_TITLE(text):
    graph_title = st.write(
        f"""
        <style>
            .normal-text {{
                text-align: left;
                font: normal normal normal 24px/28px Roboto;
                letter-spacing: 0px;
                margin-bottom: 0px;
                color: #FFFFFF;
                opacity: 1;
            }}
        </style>
        
        <div class="normal-text">{text}</div>
        """,
        unsafe_allow_html=True,
        )
    return graph_title