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
st.title("🏰 Disney California Adventure - Guest Journey Analysis")
st.write("Analysis of guest movement patterns and opportunities for improving guest experience")

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
        
        # About the Task: Guest Journey Patterns
        st.subheader("About the Task: Guest Journey Patterns")
        
        st.markdown("""
        ### **Suggested Solutions**
        
        1. Use process mining or sequence analysis to identify common guest journey paths.  
        2. Compare these patterns across segments to uncover opportunities for personalization and operational improvements.  
        
        ### **Solutions Implemented**
        
        1. **Sequence & Network Analysis**  
        - Identified frequent multi-attraction sequences (e.g., `7 → 18`) and built a transition network using NetworkX to analyze guest flow.  
        - Segmented paths by attraction themes (e.g., Family, Thrill Rides) to compare movement patterns.  
        
        2. **Opportunity Zone Mapping**  
        - Combined sequence data with places of interest (POI) to highlight underutilized areas near high-traffic attractions using KDTree spatial analysis.  
        
        3. **Cost-Profit Analysis**  
        - Assessed travel cost (based on distance) between attractions/POIs.  
        - Evaluated the potential profit (based on attraction popularity) gained from reaching specific POIs, optimizing guest flow strategies.  
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
        st.header("Guest Journey Patterns")
        st.write("Analysis of common paths taken by visitors through the park (journeys must contain non-repititive transitions)")
        
        journey_patterns, top_patterns = analyze_journey_patterns(df, poi)
        
        # Display top patterns in a nice table
        st.subheader("Top 10 Journey Patterns")
        
        pattern_df = pd.DataFrame(top_patterns, columns=["Journey", "Count"])
        st.table(pattern_df)
        
        # Summary stats
        st.write(f"Total unique journey patterns: {len(journey_patterns)}")
        
        # Business Insights & Recommendations
        st.markdown("""
        ## Business Insights & Recommendations from Popular Pairings & Guest Flow
        Based on the top journey patterns, we can derive key insights about guest behavior, optimize operations, and enhance revenue opportunities.
        """)
        
        with st.expander("### 1. Key Insights", expanded=True):
            st.markdown("""
            ### A. Popular Attraction Pairings  
            - **Radiator Springs Racers (RSR)** is a major traffic driver, frequently paired with:  
              - **Disney Junior - Live on Stage!** (8x)  
              - **The Bakery Tour** (8x)  
            - **Disney Junior - Live on Stage!** is a strong family/kiddie attraction, often leading to:  
              - **The Bakery Tour** (7x)  
              - **The Little Mermaid Ride** (7x)  
            - **The Bakery Tour** is a high-traffic secondary attraction, commonly followed by:  
              - **King Triton's Carousel** (7x)  

            *Note: The Bakery Tour is not a very popular attraction, it is just more popular for photos so we will use it cautiously for our insights.*
            """)
            
            st.markdown("""
            ### B. Guest Flow Trends  
            - **Families with young children** dominate these paths (Disney Junior + Carousel + Little Mermaid).  
            - **Food & Ride Combos**: Bakery Tour acts as a "resting spot" between rides.  
            - **RSR as a Crowd Puller**: Guests often pair high-thrill rides (RSR) with low-intensity shows (Disney Junior) or food experiences (Bakery Tour).  
              - Possible reason: Guests tire of waiting for RSR (70 min avg wait time in 2015 vs <10 mins for others ([source](https://queue-times.com/parks/17/stats/2015)))
            """)
        
        with st.expander("### 2. Strategic Recommendations", expanded=False):
            cols = st.columns(2)
            with cols[0]:
                st.markdown("""
                ### A. Optimize Queue & Crowd Management  
                - Extend RSR FastPass/Genie+ Slots to reduce congestion  
                - Deploy Mobile Food Carts near Disney Junior exit  
                """)
                
                st.markdown("""
                ### B. Enhance Cross-Promotion  
                - Bundle Experiences: "Family Fun Pack" (RSR + Disney Junior + Bakery Tour)  
                """)
            
            with cols[1]:
                st.markdown("""
                ### C. Increase F&B Revenue  
                - Upsell Bakery Tour samples as premium add-ons  
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
            | Initiative               | Cost       | Daily Revenue | Monthly ROI  |
            |--------------------------|-----------|---------------|-------------|
            | Mobile Food Cart         | $5k       | $2,500        | $70k net    |
            | Family Fun Pack Bundle   | $0        | $2,500        | $75k profit |
            """)
            st.caption("Data sources: [Queue Times](https://queue-times.com), [AECOM Report](https://aecom.com/content/wp-content/uploads/2015/10/2014_Theme_Index.pdf)")
             
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

        st.write("Identifying underutilized areas near popular attractions to disperse guests at top attractions and serve as strong complements")

        st.markdown("""
        Note: Not all top attractions (stars) here correspond to the actuals top attractions. The data used is based on number of photos taken, which favour more photogenic attractions.
        
        - This is just a proof of concept with some suggested theoretical insights. 
        - Actual results may differ based on the specific data used.
        """)
        
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
        - The smaller the red point, the bigger the potential as an effective opportunity zone (underutilized area)
        
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
            "ROI": ["$70,000 (1400%)", "$75,000"]
        }
        
        roi_df = pd.DataFrame(roi_data)
        st.table(roi_df)

    # Page 6: Cost-Profit Analysis
    elif page == "Cost-Profit Analysis":
        st.header("Cost-Profit Analysis of Attraction Routes")
        st.subheader("Calculated using distance as cost, and attraction popularity as profit")

        # Load data
        cost_profit_df = load_cost_profit_data("data/A3/costProfCat-caliAdv-all.csv")
        insights = get_cost_profit_insights(cost_profit_df)

        # Summary Insights
        st.markdown("### Key Findings")
        for observation in insights["summary"]:
            st.markdown(f"- {observation}")
        
        # Layout Optimization
        tab1, tab2 = st.tabs(["Most Cost-Effective Routes", "Most Popular Routes"])
        
        with tab1:
            st.subheader("Top 5 Most Cost-Effective Routes")
            st.dataframe(insights["top_efficient"][['from', 'to', 'distance', 'popularity', 'cost_effectiveness']])
            
            st.markdown("#### Why These Routes Stand Out")
            st.markdown("""
            **1. Turtle Talk with Crush → Animation Academy**  
            - **Cost-effectiveness**: 145.38  
            - Shortest distance (32.3m), maximizing efficiency  
            - Both are engaging, family-friendly indoor experiences  
            - Long combined ride duration (2100s)  

            **2. Red Car Trolley & News Boys → Disney Junior - Live on Stage!**  
            - **Cost-effectiveness**: 117.26  
            - Moderate distance (56.03m) with high popularity (6570)  
            - Combines a moving ride and a live stage show for variety  
            """)
        
        with tab2:
            st.subheader("Top 5 Most Popular Routes")
            st.dataframe(insights["top_popular"][['from', 'to', 'distance', 'popularity', 'cost_effectiveness']])
            
            st.markdown("#### Why These Routes Attract the Most Visitors")
            st.markdown("""
            **Key Trend:** Every top route leads to **The Little Mermaid ~ Ariel's Undersea Adventure**, confirming its status as the most in-demand attraction.  
            
            **1. Tower of Terror → The Little Mermaid**  
            - **Longest distance** (426.44m)  
            - Combines two high-thrill dark rides  
            - **Lowest cost-effectiveness** (17.97) but extremely high demand  

            **2. Ladybug Boogie → The Little Mermaid**  
            - Medium distance (365.04m)  
            - Transition from a light kiddie ride to a major family ride  
            
            **3. Mater’s Junkyard Jamboree → The Little Mermaid**  
            - **Shortest distance** in this group (224.79m)  
            - Best cost-effectiveness (34.09)  
            """)
        
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
