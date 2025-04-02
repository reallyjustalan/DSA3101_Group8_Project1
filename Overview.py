import streamlit as st
import streamlit_mermaid as st_mermaid
from streamlit.components.v1 import html

def main():
    st.set_page_config(layout="wide", page_title="Theme Park Optimization Dashboard")
    
    # Header with logo/title
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://github.com/user-attachments/assets/258a5fb9-07de-4c76-8b7d-d2780e7766b3", 
                width=150)
    with col2:
        st.title("Theme Park Optimization Intelligence")
    
    st.subheader(":sparkles: Where Data Science Meets Magical Experiences :sparkles:")

    # Hero section
    st.markdown("""
    <div style='background-color:#2a3f5f; padding:25px; border-radius:10px; margin-bottom:25px;'>
        <h3 style='color:white; margin-bottom:10px;'>The Global Amusement Park Industry is Growing at 10.55% CAGR</h3>
        <p style='color:#f0f2f6; font-size:16px;'>Our data-driven solutions reveal how to simultaneously elevate guest satisfaction and operational efficiency in this complex ecosystem.</p>
    </div>
    """, unsafe_allow_html=True)

    # Core value proposition
    st.header("Our Interconnected Insights Framework")
    st.write("""
    We've developed 10 integrated solutions across two domains that create a virtuous cycle 
    between guest experience and operations:
    """)

    # Mermaid diagram using the streamlit-mermaid component
    st.subheader("How Our Solutions Work Together")
    
    mermaid_code = """
    %%{init: {'theme': 'base', 'themeVariables': { 'arrowheadColor': '#cccccc', 'arrowLabelBackground': '#f8f8f8', 'edgeLabelBackground':'#f8f8f8'}}}%%
    flowchart TD
        linkStyle default stroke:#cccccc,stroke-width:2px,fill:none
        A1[A1: Guest Satisfaction] --> B3
        A1 --> B2
        A3[A3: Guest Journey] --> B2
        B5[B5: IoT Data Integration] --> A3
        B4[B4: Guest Complaint Prediction] --> A1
        B5 --> B2[B2: Attraction Layout Optimization]
        B5 --> B3[B3: Variable Demand Allocation]
        A5[A5: External Factors] --> B3
        A4[A4:Marketing Impact] --> A1
        B1[B1: Demand Prediction]--> B2
        A2[A2: Guest Segmentation] --> A4
        A5 --> A4
        B4 --> B3
    """
    
    st_mermaid.st_mermaid(mermaid_code, height=400)

    # Key insights highlights
    st.subheader("Key Business Impacts")
    with st.expander("See how our solutions drive value"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Guest Experience**
            - 🎢 21% satisfaction boost from attraction optimization
            - 🎯 55% hidden dissatisfaction uncovered in ratings
            - 📈 50% visitor increase from targeted campaigns
            """)
        with col2:
            st.markdown("""
            **Operations**
            - 👥 30% more efficient staff allocation
            - 🗺️ 15% reduced walk times from layout optimization
            - 📶 Real-time crowd tracking with WiFi analytics
            """)

    # Navigation guidance
    st.subheader("Explore Our Solutions")
    st.write("Here you can find a Business Question each solution is trying to answer:")
    st.write("Use the sidebar to dive deeper into each analysis")

    
    tab1, tab2 = st.tabs(["Guest Experience", "Operations"])
    with tab1:
        st.markdown("""
        - **A1: Guest Satisfaction Drivers**: What are the primary factors affecting guest satisfaction across different touchpoints of the Disneyland guest journey?

        - **A2: Guest Segmentation**: How can we use clustering to uncover distinct guest segments and reveal hidden satisfaction gaps?

        - **A3: Guest Journey**: Where are the "opportunity zones" in guest journey patterns that can help reduce wait times at high-demand attractions?
        
        - **A4: Marketing Impact**: What marketing techniques can we use to increase theme park visitors?

        - **A5: Seasonality Patterns**: How does seasonality, public holidays and visitor demographics impact theme park attendance and reviews?

        """)
    
    with tab2:
        st.markdown("""
        - **B1: Predictive Demand Modeling**: How can a predictive model be used to identify key demand drivers for theme park attractions, and guide data-driven decisions for park operators?

        - **B2: Attraction Layout Optimization**: How can we optimize the layout of a theme park to increase customer retention?

        - **B3: Dynamic Staff Allocation**: How can we optimize staff allocation in a theme park at any given time while minimizing overall staffing levels?

        - **B4: High-risk Interaction Detection**: How can we promptly address high-risk interactions to improve guest experience?

        - **B5: IoT Data Integration**: How can WiFi access points be used to improve guest experience?

        """)

    # Footer
    st.markdown("---")
    st.caption("""
    *Data-driven decisions for the world's leading theme parks | 
    [View Full Project Documentation](https://github.com/NotInvalidUsername/DSA3101_Group8_Project1/wiki)*
    """)

if __name__ == "__main__":
    main()