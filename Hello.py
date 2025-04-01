# app.py (main file)
import streamlit as st

st.set_page_config(
    page_title="Main",
    page_icon="👋",
)

st.write("# A2: Guest Segmentation Model 👋")

st.sidebar.success("Select a page above to see the models")

st.markdown(
    """
    In this section, we aim to build a segmentation model using clustering techniques, which include demographic, behavioural, and preferences-based attributes. The business question that we wish to answer is 
    How can we use clustering to uncover distinct guest segments and reveal hidden satisfaction gaps?
    
    Applied clustering and mismatch analysis on key variables, such as ratings, sentiment, and month. Although 80% of the guests rated highly (around 4.7/5), notable discrepancies exist between ratings and sentiment. 
    Around 55% show no mismatch, while 9% are extreme “over-raters” - critical in their review but still giving high ratings (mean mismatch of +6.23). Vice versa, 23% are “under-raters” (mean mismatch of -1.22).
    
    Key insight

    Even with high overall satisfaction, mismatches between ratings and review sentiment expose underlying issues in specific segments, suggesting that some guests may mask dissatisfaction or express overly critical ratings.

    Business Impact

    Target these segments with tailored follow-up and surveys, leverage season-specific service improvements, and refine engagement strategies to convert hidden dissatisfaction into loyalty. These segmentation insights also inform A4's marketing campaign strategies.
    
    **👈 Select a page from the sidebar** to see the models
    ### Plots (Exploratory Data Analysis to better understand the data.)
    ### Model 1: DBSCAN on the whole data (Behavioural and preferences-based)
    ### Model 2: KMeans on the whole data (Behavioural and preferences-based)
    ### Model 3: KMeans Analysis on Mistmach (Behavioural)
    ### Model 4: KMeans Analysis on data split by Continent (Demographic)
    ### Model 5: KMeans Analysis on data split by Visit_Type (Demographic)
    
"""
)
