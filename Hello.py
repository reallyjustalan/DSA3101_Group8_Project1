import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from analysis import (
    load_data, 
    plot_poi_map, 
    analyze_journey_patterns, 
    create_flow_network, 
    plot_flow_network,
    analyze_opportunity_zones,
    plot_opportunity_zones,
    get_business_insights
)

# Page config
st.set_page_config(
    page_title="Disney California Adventure - Guest Journey Analysis",
    page_icon="🏰",
    layout="wide"
)

# Header
st.title("🏰 Disney California Adventure - Guest Journey Analysis")
st.write("Analysis of guest movement patterns and opportunities for improving guest experience")

# Data loading (cached to prevent reloading)
@st.cache_data
def load_cached_data():
    poi_path = "data/POI-caliAdv.csv"
    visits_path = "data/userVisits-caliAdv-allPOI.csv"
    return load_data(poi_path, visits_path)

# Try to load data with error handling
try:
    poi, seq, df = load_cached_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Please make sure the data files are in the 'data' folder")
    data_loaded = False

# Only proceed if data is loaded successfully
if data_loaded:
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page:",
        ["Park Overview", "Journey Patterns", "Visitor Flow Network", "Opportunity Zones", "Business Insights"]
    )
    
    # Page 1: Park Overview
    if page == "Park Overview":
        st.header("Park Overview")
        st.write("Map of attractions at Disney California Adventure")
        
        map_fig = plot_poi_map(poi)
        st.plotly_chart(map_fig, use_container_width=True)
        
        # Basic stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Attractions", len(poi))
        with col2:
            st.metric("Unique Visitors", seq["nsid"].nunique())
        with col3:
            st.metric("Total Photo Records", len(seq))
    
    # Page 2: Journey Patterns
    elif page == "Journey Patterns":
        st.header("Guest Journey Patterns")
        st.write("Analysis of common paths taken by visitors through the park")
        
        journey_patterns, top_patterns = analyze_journey_patterns(df, poi)
        
        # Display top patterns in a nice table
        st.subheader("Top 10 Journey Patterns")
        
        pattern_df = pd.DataFrame(top_patterns, columns=["Journey", "Count"])
        st.table(pattern_df)
        
        # Summary stats
        st.write(f"Total unique journey patterns: {len(journey_patterns)}")
        
        # Add an explanation
        st.markdown("""
        ### Insights from Journey Patterns
        
        - **Popular Sequences**: The most common guest paths reveal how visitors naturally flow through the park
        - **Family-Focused Paths**: Many top journeys connect family-friendly attractions
        - **Photo Opportunity Points**: These patterns highlight where guests prefer to take photos
        """)
    
    # Page 3: Visitor Flow Network
    elif page == "Visitor Flow Network":
        st.header("Visitor Flow Network")
        st.write("Network visualization of guest movement between attractions")
        
        # Get the journey patterns and create network
        journey_patterns, _ = analyze_journey_patterns(df, poi)
        poi_name_map = dict(zip(poi['poiID'].astype(str), poi['poiName']))
        
        # Create network with different sizes
        top_n = st.slider("Number of top connections to show", 10, 100, 50)
        G, filtered_edges = create_flow_network(journey_patterns, poi_name_map, top_n=top_n)
        
        # Plot the network
        flow_fig = plot_flow_network(G, filtered_edges)
        st.pyplot(flow_fig)
        
        # Add explanation
        st.markdown("""
        ### Understanding the Flow Network
        
        - **Nodes**: Attractions in the park
        - **Edges**: Guest movement between attractions
        - **Edge Weight**: Number of transitions between attractions
        - **Red Node**: Radiator Springs Racers (ID 14), a major hub
        
        This visualization helps identify key traffic patterns and potential bottlenecks.
        """)
    
    # Page 4: Opportunity Zones
    elif page == "Opportunity Zones":
        st.header("Opportunity Zones Analysis")
        st.write("Identifying underutilized areas near popular attractions")
        
        # Run the opportunity zone analysis
        plot_df, top_coords, far_percentage = analyze_opportunity_zones(df)
        
        # Plot the opportunity zones
        opp_fig = plot_opportunity_zones(plot_df, top_coords, far_percentage)
        st.pyplot(opp_fig)
        
        # Add explanation
        st.markdown(f"""
        ### Key Insights
        
        - **{far_percentage:.1f}%** of photos are taken more than 100m from top attractions
        - **Green circles** highlight opportunity zones - underutilized areas near popular spots
        - **Gold stars** mark the top attractions by visitor photos
        - **Red points** show locations within 100m of popular attractions
        
        These opportunity zones represent potential areas for:
        - New food & beverage locations
        - Merchandise stands
        - Photo opportunities
        - Character meet-and-greets
        - Rest areas or additional amenities
        """)
    
    # Page 5: Business Insights
    elif page == "Business Insights":
        st.header("Business Insights & Recommendations")
        
        insights = get_business_insights()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Popular Attraction Pairings")
            for insight in insights["popular_pairings"]:
                st.markdown(f"- {insight}")
                
            st.subheader("Guest Flow Trends")
            for trend in insights["guest_flow_trends"]:
                st.markdown(f"- {trend}")
        
        with col2:
            st.subheader("Strategic Recommendations")
            for rec in insights["recommendations"]:
                st.markdown(f"- {rec}")
                
            st.subheader("Top Opportunity Zones")
            for zone in insights["opportunity_zones"]:
                st.markdown(f"- {zone}")
        
        # Add ROI estimates
        st.subheader("Estimated ROI for Recommendations")
        
        roi_data = {
            "Initiative": ["Mobile Food Cart Near Disney Junior", "Family Fun Pack Bundle"],
            "Cost": ["$5,000", "$0 (existing infrastructure)"],
            "Monthly Revenue": ["$75,000", "$75,000"],
            "ROI": ["$70,000 (1400%)", "$75,000 (∞)"]
        }
        
        roi_df = pd.DataFrame(roi_data)
        st.table(roi_df)

# Footer
st.markdown("---")
st.markdown("Data source: Geo-tagged Flickr photos from Disney California Adventure (2007-2017)")
