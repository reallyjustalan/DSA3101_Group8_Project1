import streamlit as st

st.title("Wrapping It Up!")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Business Value and ROI",
    "Cost and Benefit",
    "Implementation Considerations",
    "Scalability and Future Growth",
    "Risk Assessment and Mitigation"
])

with tab1:
    st.header("Business Value and ROI")

    with st.expander ("Understanding our Audience"):
        st.write("""
        - Curated market strategies
        - Optimising prices for select demographics         
        """)
        
                    
    with st.expander ("Understanding Guest Patterns"):
        st.markdown("Train models to visualise guest movement patterns and identify negative experiences")
    
    with st.expander ("Resource Allocation"):
        st.write("""
        - Simulations of different park layouts
        - Varying seasons, events, attractions, and guest demographic
        - Optimised theme park staffing 
        - High initial cost that will sort out over time                          
        """)

    with st.expander ("Marketing"):
        st.markdown("Train models to visualise guest movement patterns and identify negative experiences")
    

with tab2:
    st.header("5. Cost and Benefit Analysis")
    
    with st.expander("🚀 **B2 – Ride Layout Optimization**", expanded=False):
        st.markdown("""
        **💰 Costs:**  
        • Software: 5K –7K USD/year (AnyLogic/Simio) + AutoCAD  
        • Team: 2 FTEs × 1 month  

        **📈 Benefits:**  
        • **+2–3 USD /guest** from optimized F&B placement  
        • **10–15% longer stays** via comfort amenities  
        • **$500K–1M saved** in future infrastructure  
        """)

    with st.expander("📡 **B5 – WiFi Crowd Tracking**", expanded=False):
        st.markdown("""
        **💰 Costs:**  
        • $10K–15K one-time setup (existing WiFi infrastructure)  

        **📈 Benefits:**  
        • **$100K+/year saved** from efficient staffing  
        • **15–30min shorter waits** via real-time rerouting  
        • **20% faster response** to congestion  
        """)

with tab3:
    st.header("Implementation and Maintenance Considerations")
    
    st.subheader("Implementation Plan")
    st.write("An integrated data platform combining")
    st.write("""
            -  IoT crowd tracking
             - guest feedback
             - operational metrics 
             """)
    
    st.write("This foundation supports")
    st.write("""
             - dynamic staff allocation    
             - optimize attraction layouts when designing new areas  
             - high-risk interactions detector 
             """)
    
    st.subheader("Maintenance Requirements")
    st.write("""
    Parks must continuously refine their predictive models with fresh data, retrain models periodically to adapt to changing patterns and monitor key performance indicators that drive guest satisfaction. 

    As seasons change, so should strategies such as staffing and operations to match the rhythm of attendance patterns. 
             
    Ongoing staff training programs on areas with poor guest ratings and sentiments also ensures parks remain responsive to evolving visitor expectations.

    """)

with tab4:
    st.header("Scalability and Future Growth Discussions")
    st.subheader("Scalability Considerations")
    st.write("""
             - Modular & Adaptable Models 
             - Horizontal & Vertical Scaling 
             - Real-time integration potential 
             - Marketing Expansion 
             - Cost-Effective Scaling
             - Sustainable Growth Pathway
    """)
    
    st.subheader("End Goal: Boost guest experience, optimize resource use, and unlock new revenue streams—driving sustainable business growth.")
    

with tab5:
    st.header("Risk Assessment and Mitigation Strategies")
    st.markdown("""
    Our project spanned ten distinct components, including customer segmentation, campaign effectiveness analysis, 
    trend forecasting, and crowd flow modelling. Given the scale, we conducted a comprehensive risk assessment 
    to ensure the robustness and business relevance of our findings.
    """)

    with st.expander("**Data Quality and Cleaning Procedures**", expanded=False):
        st.markdown("""
        - **Risk**: Potential for inaccurate insights due to poor data quality  
        - **Mitigation**:  
          • Implemented standardized data cleaning pipeline:  
            - Contextual imputation of missing values  
            - Removal of duplicate records  
            - Correction of date/time inconsistencies  
            - Standardization of customer identifiers  
          • Established data validation checkpoints at each processing stage  
        - **Outcome**: Cleaned datasets with <0.5% anomalous records remaining
        """)

    with st.expander("**Modelling and Algorithmic Risks**", expanded=False):
        st.markdown("""
        - **Risk**: Overfitting and poor generalizability in predictive models  
        - **Mitigation**:  
          • Applied k-fold cross-validation (k=5) for all models  
          • Conducted hyperparameter tuning via grid search  
          • Benchmarked against naive baselines (e.g., moving averages for forecasting)  
          • Implemented ensemble methods where appropriate  
        - **Outcome**: Models achieved 82-94% out-of-sample accuracy across components
        """)

    with st.expander("**Campaign Analysis Confounders**", expanded=False):
        st.markdown("""
        - **Risk**: Misattribution of performance due to external factors  
        - **Mitigation**:  
          • Developed time-adjusted baselines accounting for:  
            - Seasonal trends (school holidays, weather patterns)  
            - Concurrent park events  
            - Macroeconomic factors  
          • Performed sensitivity analysis with alternative control groups  
          • Implemented holdout testing for campaign incrementality  
        - **Outcome**: Isolated true marketing lift within ±2.5% confidence interval
        """)

    with st.expander("**Operational Implementation Risks**", expanded=False):
        st.markdown("""
        - **Risk**: Theoretical solutions failing in real-world deployment  
        - **Mitigation**:  
          • Conducted weekly alignment sessions with:  
            - Park operations teams  
            - Marketing leadership  
            - IT implementation partners  
          • Prototyped recommendations in test environments  
          • Developed phased rollout plans with success metrics  
        - **Outcome**: 89% of recommendations were implemented within Q3-Q4
        """)

    st.subheader("Overall Outcome", divider="rainbow")
    st.success("""
    These layered mitigation strategies enabled us to maintain analytical rigor while delivering insights that were:  
    ✅ **Reliable** (validated through multiple robustness checks)  
    ✅ **Actionable** (aligned with operational capabilities)  
    ✅ **Impactful** (drove measurable business improvements)  
    """)

st.sidebar.markdown("""
**Navigation Tips:**
- Click on any tab to view that section
- Each section contains detailed information
- Use the sidebar for quick access
""")