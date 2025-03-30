# app.py (main demo file)
import streamlit as st
from guest_journey import plot_journey_network, plot_opportunity_zones, insights

st.set_page_config(layout="wide")
st.title("🏰 Disney California Adventure Guest Journey Analysis")

tab1, tab2 = st.tabs(["Journey Patterns", "Opportunity Zones"])

with tab1:
    plot_journey_network()
    insights()

with tab2:
    plot_opportunity_zones()
    st.write("")  # Spacer
    with st.expander("📊 Data Interpretation"):
        st.markdown("""
        - **Red circles**: Underutilized attractions near popular spots
        - **Gold stars**: Top 20% most photographed attractions
        - **Green rings**: 100m opportunity zones around hotspots
        """)
