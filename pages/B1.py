import streamlit as st 
from PIL import Image
import os

st.set_page_config(page_title="Demand Prediction - B1", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("📂 Navigate to section:", [
    "📌 Overview",
    "📊 Dataset & Predictors",
    "⚙️ Model & Performance",
    "📈 Business Insights",
    "🚧 Limitations & Improvements"
])

# -------------- Page: Overview ----------------
if page == "📌 Overview":
    st.title("🎯 Executive Summary")
    
    st.markdown("""
    ## 🧠 Key Insight
    The optimal predictive model revealed that **attraction-specific appeal is the strongest driver** of demand, surpassing external factors like weather or holidays.

    ## 💡 Unique Value Proposition
    Our model empowers operators to **move from reactive to proactive** decisions—guiding enhancements to high-impact attractions over mitigating uncontrollable conditions.

    ## 🛠️ Implementation & Practicality
    - Use **ticket scan data** and **ride entry counts** for direct demand signals.
    - Integrate **explainability tools** like SHAP to understand drivers of demand.
    - Guide decisions on **enhancements**, **weatherproofing**, and **staffing** based on forecasted demand.

    ## 📈 Potential ROI
    Informs strategic planning in:
    - **B2**: Layout optimization
    - **B3**: Resource allocation
    
    Leading to **increased revenue**, **improved guest experience**, and **greater operational efficiency**.
    """)

# -------------- Page: Dataset & Predictors ----------------
elif page == "📊 Dataset & Predictors":
    st.title("🛠️ Dataset & Predictors")

    st.markdown("We selected predictors that reflect both internal drivers and external influences on attraction demand:")

    with st.expander("🎢 Predictor 1: Total Fatalities in Disney Theme Parks"):
        st.markdown("High-profile incidents may affect public confidence, causing sudden drops in demand.")

    with st.expander("🌧️ Predictor 2: Weather (Rainy and Non-Rainy Days)"):
        st.markdown("Weather impacts outdoor attraction turnout. Rainy-day proportions capture demand dips during bad conditions.")

    with st.expander("🌪️ Predictor 3: Natural Disasters"):
        st.markdown("Disasters like storms or hurricanes disrupt park operations and reduce turnout.")

    with st.expander("🏖️ Predictor 4: Number of Public Holidays in Each Month"):
        st.markdown("More public holidays generally boost family outings and park visits.")

    with st.expander("🍂 Predictor 5: Seasons (Spring, Summer, Fall, Winter)"):
        st.markdown("Captures peak travel periods (e.g., summer holidays) vs. off-peak times.")

    with st.expander("🎆 Predictor 6: Average Number of Night Shows per Month"):
        st.markdown("Night shows extend guest stay and increase park value perception.")

    with st.expander("🎡 Predictor 7: Market Competition (SeaWorld Orlando Visitor Numbers)"):
        st.markdown("Competitor attendance reflects external pressures and shared market trends.")

# -------------- Page: Model & Performance ----------------
elif page == "⚙️ Model & Performance":
    st.title("📈 Model Selection & Performance")
    
    st.markdown("### 🔍 Models Evaluated")
    st.markdown("""
    We compared six models, balancing interpretability and performance:
    - Linear, Ridge, Lasso, Elastic Net
    - Decision Tree, Random Forest
    """)

    st.markdown("### ⚙️ Evaluation Method")
    st.markdown("""
    - **5-Fold Cross-Validation** for robustness
    - **Grid Search** for tuning hyperparameters
    - Metrics used:
        - **RMSE** (penalizes large errors)
        - **MAE** (average absolute error)
    """)

    st.markdown("### 📊 Performance Metrics")
    col1, col2 = st.columns(2)

    with col1:
        image_path_RMSE = os.path.join(os.path.dirname(__file__), "..", "data", "B1", "CV_RMSE.png")
        if os.path.exists(image_path_RMSE):
            st.image(Image.open(image_path_RMSE), caption="5-Fold CV RMSE by Model", width=550)
        else:
            st.error("RMSE image not found.")

    with col2:
        image_path_MAE = os.path.join(os.path.dirname(__file__), "..", "data", "B1", "CV_MAE.png")
        if os.path.exists(image_path_MAE):
            st.image(Image.open(image_path_MAE), caption="5-Fold CV MAE by Model", width=550)
        else:
            st.error("MAE image not found.")

    st.success("Random Forest was selected based on lowest RMSE & MAE.")

# -------------- Page: Business Insights ----------------
elif page == "📈 Business Insights":
    st.title("📊 Business Insights from Model Output")

    image_path_feature_imp = os.path.join(os.path.dirname(__file__), "..", "data", "B1", "feature_imp.png")
    if os.path.exists(image_path_feature_imp):
        st.image(Image.open(image_path_feature_imp), caption="Top 10 Feature Importances", width=700)
    else:
        st.error("Feature importance image not found.")

    with st.expander("🔎 Key Findings"):
        st.markdown("""
        - **Top attractions** like Log Flume, Merry-Go-Round, and Dizzy Dropper were the strongest predictors.
        - These outweighed weather, suggesting **ride appeal trumps weather risk**.
        - Visitors are likely to visit these high-appeal rides even in less favourable weather conditions.
        
        **Recommendations:**
        - Invest in enhancing popular rides
        - Add shelters near weather-sensitive zones
        - Use predictions to adjust staffing and operations
        """)

# -------------- Page: Limitations & Improvements ----------------
elif page == "🚧 Limitations & Improvements":
    st.title("⚠️ Limitations & Improvements")

    with st.expander("🔍 Identified Limitations"):
        st.markdown("""
        - **Estimated Demand:**
            - Based on **queue wait times and ride visitor counts**—not direct indicators.
            - May reflect congestion or staffing issues rather than true popularity.

        ➤ *Future models should use direct metrics like ticket scans, ride entries, or app tracking.*

        - **Model Transparency:**
            - Random Forests lack interpretability.
            - Harder for stakeholders to grasp why predictions are made.

        ➤ *Incorporate tools like SHAP or LIME to enhance explainability for decision-makers.*
        """)

    st.info("Improving data quality and explainability will increase operational usefulness and stakeholder trust.")
