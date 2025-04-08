import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from scripts.A3.journey_analysis import (
    load_data, 
    plot_poi_map, 
    analyze_journey_patterns, 
    create_flow_network, 
    plot_flow_network,
    analyze_opportunity_zones,
    plot_opportunity_zones,
    get_business_insights
)
from scripts.A3.cost_profit_analysis import (load_cost_profit_data, plot_cost_profit_scatter, get_cost_profit_insights
)

# Page config
st.set_page_config(
    page_title="Disney California Adventure - Guest Journey Analysis",
    page_icon="🏰",
    layout="wide"
)

# Header
st.title("🚶🏽‍♂️ Guest Journey Analysis ")
st.write("Analysis of guest movement patterns and opportunities for improving guest experience in Disney California Adventure 🏰")

# Data loading (cached to prevent reloading)
@st.cache_data
def load_cached_data():
    poi_path = "data/A3/POI-caliAdv.csv"
    visits_path = "data/A3/userVisits-caliAdv-allPOI.csv"
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
        ["Overview", "Journey Patterns", "Visitor Flow Network", "Opportunity Zones", "Business Insights", "Cost-Profit Analysis"]
    )
    
    # Page 1: Overview
    if page == "Overview":
        st.header("Overview")
        
        # About the Solutions
        st.subheader("About the Solutions:")
        
        st.markdown("""
                
        1. **Sequence & Network Analysis**  
        - Identified frequent multi-attraction sequences and built a transition network using NetworkX to analyze guest flow.  
        - Segmented paths by attraction themes (e.g., Family, Thrill Rides) to compare movement patterns.  
        
        2. **Opportunity Zone Mapping**  
        - Highlight underutilized areas near high-traffic attractions that could better complement high-demand attractions.
        
        3. **Cost-Profit Analysis**  
        - Assessed travel cost (based on distance) between attractions/POIs.  
        - Evaluated the potential profit (based on attraction popularity) of different routes.
        """)


        st.subheader("About the Park: Disney California Adventure")

        # Map visualization
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
        st.header("🧩 Guest Journey Patterns")
        st.write("Analysis of common paths taken by visitors through the park (journeys must contain non-repetitive transitions)")
        
        journey_patterns, top_patterns = analyze_journey_patterns(df, poi)
        
        # Display top patterns in a nice table
        st.subheader("Top 10 Journey Patterns")
        
        pattern_df = pd.DataFrame(top_patterns, columns=["Journey", "Count"])
        st.table(pattern_df)
        
        # Summary stats
        st.write(f"Total unique journey patterns: {len(journey_patterns)}")
        
        # Business Insights & Recommendations
        st.markdown("""
        ## 💡 Business Insights & Recommendations
        Based on the top journey patterns, we can derive key insights about guest behavior, optimize operations, and enhance revenue opportunities.
        """)
        
        with st.expander("### 1. Key Insights", expanded=True):
            st.markdown("""
            - The count of popular journeys do not make up a large portion of the total number of journeys, suggesting a good park layout, preventing overcrowding.
            - **RSR as a Crowd Puller**: Guests often pair high-thrill rides (RSR) with low-intensity shows (Disney Junior) or food experiences (Bakery Tour).  
              - Possible reason: Guests tire of waiting for RSR (70 min avg wait time in 2015 vs <10 mins for others ([source](https://queue-times.com/parks/17/stats/2015)))    
            """)
        
        
        with st.expander("### 2. Strategic Recommendations", expanded=False):
            cols = st.columns(2)
            with cols[0]:
                st.markdown("""
                ### A. Optimize Queue & Crowd Management  
                - Extend RSR FastPass/Genie+ Slots to reduce congestion  
                """)
                
                st.markdown("""
                ### B. Enhance Cross-Promotion  
                - Bundle Experiences: "Family Fun Pack" (RSR + Disney Junior + Bakery Tour)  
                """)
            
            with cols[1]:
                st.markdown("""
                ### C. Increase F&B Revenue  
                - Deploy Mobile Food Carts near Disney Junior exit   
                - Place snack kiosks between Carousel and Little Mermaid  
                """)
                
                st.markdown("""
                ### D. Improve Show Scheduling  
                - Align Disney Junior showtimes with RSR ride exits  
                """)
        
        with st.expander("### 3. Success KPIs & ROI", expanded=False):
            st.markdown("""
            #### Key Performance Indicators
            | Objective               | KPI                          | Target       |
            |-------------------------|------------------------------|-------------|
            | Increase Guest Spending | Avg. F&B spend per guest     | +15%        |
            | Improve Attraction Flow | Wait time reduction at RSR   | -20%        |
            | Guest Satisfaction      | Post-experience survey       | ≥4.5/5      |
            """)
            
            st.markdown("""
            #### ROI Calculations (Based on 2015 attendance)
            | Initiative               | Monthly Cost       | Daily Revenue | Monthly ROI  |
            |--------------------------|-----------|---------------|-------------|
            | Mobile Food Cart         | $5k       | $2,500        | $70k net    |
            | Family Fun Pack Bundle   | $0        | $2,500        | $75k profit |
            """)
            st.caption("Data sources: [Queue Times](https://queue-times.com), [AECOM Report](https://aecom.com/content/wp-content/uploads/2015/10/2014_Theme_Index.pdf)")
             
    # Page 3: Visitor Flow Network
    elif page == "Visitor Flow Network":
        st.header("🌐 Visitor Flow Network")
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
        - **Red Node**: Most popular attraction
        
        This visualization helps identify key traffic patterns and potential bottlenecks.
        """)
    
    # Page 4: Opportunity Zones
    elif page == "Opportunity Zones":
        st.header("Opportunity Zones Analysis")

        st.write("Instead of adding more rides nearby (which could create competition), strategically activating underutilized areas nearby can extend the guest experience and capture additional spending.")

        st.write("This analysis aims to complement B2 which plans the optimal park layout.")

        st.markdown("""
        **Note**: This is just a proof of concept with some suggested theoretical insights, actual results may differ based on the specific data used.
        """)
        
        # Run the opportunity zone analysis
        plot_df, top_coords, far_percentage = analyze_opportunity_zones(df)
        
        # Plot the opportunity zones
        opp_fig = plot_opportunity_zones(plot_df, top_coords, far_percentage)
        st.pyplot(opp_fig)
        
        # Add explanation
        st.markdown(f"""
        ### Key Insights
        
        - **{far_percentage:.1f}%** of photos are taken more than 100m from top attractions, suggesting an imbalance
        - The smaller the red point, the bigger the potential as an effective opportunity zone (underutilized area)
        
        These opportunity zones represent potential areas for:
        - New F&B locations
        - Merchandise stands
        - Photo opportunities
        - Character meet-and-greets
        - Rest areas or additional amenities
        """)
    
    # Page 5: Business Insights
    elif page == "Business Insights":
        st.header("Business Insights & Recommendations")
        

        st.write("To optimize guest flow and revenue, focus on **complementing** top attractions rather than competing with them. By strategically activating nearby underutilized areas, we can enhance the guest experience and drive additional spending.")  

        with st.expander("Key Insight 🎢"):  
            st.write("Top attractions like Radiator Springs Racers (RSR) create natural guest congestion. Instead of adding more rides nearby, activating underutilized areas can **extend guest experience** and **increase spending**.")  

        with st.expander("Unique Value Proposition 🚀"):  
            st.write("- Enhances guest experience without direct competition.\n"  
                    "- Eases congestion while boosting per-guest revenue.\n"  
                    "- Encourages longer guest dwell time in key areas.")  

        with st.expander("Implementation 🏗️"):  
            st.write("- **F&B & Retail:** Themed food carts & pop-ups near attraction exits.\n"  
                    "- **Interactive Zones:** Character meet-and-greets or mini-activities.\n"  
                    "- **Timed Mini-Shows:** Quick entertainment aligned with peak guest movement.")  

        with st.expander("Potential ROI 📈"):  
            st.write("- **15-20%** increase in per-guest spending.\n"  
                    "- Reduced dissatisfaction from long wait times.\n"  
                    "- Balanced guest flow, reducing strain on main attractions.")  

        st.write("This strategy ensures a seamless, immersive experience while optimizing revenue potential.")  


    # Page 6: Cost-Profit Analysis
    elif page == "Cost-Profit Analysis":
        st.header("Cost-Profit Analysis of Attraction Routes")
        st.write("Calculated using distance as cost, and attraction popularity as profit")

        # Load data
        cost_profit_df = load_cost_profit_data("data/A3/costProfCat-caliAdv-all.csv")
        insights = get_cost_profit_insights(cost_profit_df)

        # Summary Insights
        with st.expander("### Key Findings"):
            for observation in insights["summary"]:
                st.markdown(f"- {observation}")
        
        # Layout Optimization
        tab1, tab2 = st.tabs(["Most Cost-Effective Routes", "Most Popular Routes"])
        
        with tab1:
            st.subheader("Top 5 Most Cost-Effective Routes")
            st.dataframe(insights["top_efficient"][['from', 'to', 'distance', 'popularity', 'cost_effectiveness']])
            

        with tab2:
            st.subheader("Top 5 Most Popular Routes")
            st.dataframe(insights["top_popular"][['from', 'to', 'distance', 'popularity', 'cost_effectiveness']])
        
        # Business Recommendations
        st.subheader("📌 Business Recommendations")
        st.markdown("""
        - **Enhance signage and pathways** to The Little Mermaid to manage high traffic.  
        - **Promote efficient ride/show combinations** (e.g., Turtle Talk + Animation Academy).  
        - **Create bundled experiences** for top cost-effective routes.  
        - **Improve amenities** along popular long-distance routes to enhance visitor comfort.  
        """)
        
        # Data Visualizations
        st.subheader("📊 Data Distributions")
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        sns.histplot(cost_profit_df['distance'], bins=30, kde=True, ax=axes[0])
        axes[0].set_title('Distribution of Distance')
        sns.histplot(cost_profit_df['popularity'], bins=30, kde=True, ax=axes[1])
        axes[1].set_title('Distribution of Popularity')
        sns.histplot(cost_profit_df['rideDuration'], bins=30, kde=True, ax=axes[2])
        axes[2].set_title('Distribution of Ride Duration')
        st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Data source: Geo-tagged Flickr photos from Disney California Adventure (2007-2017)")
