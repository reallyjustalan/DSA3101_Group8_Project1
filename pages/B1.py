import streamlit as st 
from PIL import Image
import os

st.set_page_config(page_title="Demand Prediction - B1", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["Creating the dataset", "Modelling", "Business Insights", "Limitations & Improvements"]
)

# ------------------ Page: Creating the dataset ------------------
if page == "Creating the dataset":
    st.title("🛠️ Creating the Dataset for Demand Prediction")
    st.markdown("### 📌 Selected Predictors and Rationale")

    st.markdown("""
    To build an effective demand prediction model for attractions and services, we incorporated predictors that capture both **internal performance factors** and **external influences** like weather, public sentiment, and competition. Here's a breakdown of the key predictors used and why they were chosen:
    
    - **Predictor 1: Total Fatalities in Disney Theme Parks (By Year)**  
      While rare, high-profile incidents may influence public perception and visitor confidence. Including this accounts for sudden drops in demand due to safety concerns.

    - **Predictor 2: Weather (Rainy and Non-Rainy Days)**  
      Weather has a direct impact on outdoor attraction attendance. We included rainy-day proportions to capture fluctuations in demand due to unfavorable conditions.

    - **Predictor 3: Natural Disasters**  
      Events like hurricanes or storms could lead to operational shutdowns or deter visitor turnout. This variable captures the intensity of such disruptions.

    - **Predictor 4: Number of Public Holidays in Each Month**  
      More public holidays typically increase family outings and travel, which positively correlates with demand at theme parks.

    - **Predictor 5: Seasons (Spring, Summer, Fall, Winter)**  
      Seasonal effects help us capture peak tourism periods (e.g. summer holidays or spring breaks) vs. off-peak months.

    - **Predictor 6: Average Number of Night Shows (Disney Events) per Month and Year**  
      Night shows can boost visitor numbers by extending park hours and enhancing value for guests. This measures Disney’s in-park engagement strategy.

    - **Predictor 7: Market Competition (SeaWorld Orlando Visitor Numbers)**  
      As a nearby competitor, fluctuations in SeaWorld’s attendance may reflect shared market trends or competition for footfall, offering insights into external pressure on demand.
    """)

# ------------------ Page: Modelling ------------------
elif page == "Modelling":
    st.title("🔍 Modelling Approach & Evaluation")
    
    st.markdown("### Models Evaluated")
    st.markdown("""
    We assessed six machine learning models to predict attraction demand based on curated predictors:

    - **Linear Regression**
    - **Ridge Regression**
    - **Lasso Regression**
    - **Elastic Net Regression**
    - **Decision Tree Regression**
    - **Random Forest Regression**

    These models were chosen to balance interpretability (linear models) and predictive power (tree-based models).
    """)

    st.markdown("### Methodology")
    st.markdown("""
    - We employed **5-Fold Cross-Validation (CV)** to ensure model robustness across different data splits.
    - For models with hyperparameters (e.g. Ridge, Lasso, Elastic Net, Decision Tree, Random Forest), we performed **Grid Search CV** to select optimal configurations.
    - Models were evaluated using:
        - **RMSE (Root Mean Squared Error)**: Penalizes large prediction errors
        - **MAE (Mean Absolute Error)**: Measures average absolute difference between predicted and true values
    """)

    st.markdown("### Performance Comparison")

    col1, col2 = st.columns(2)

    # CV RMSE & MAE images for models
    with col1:
        image_path_RMSE = os.path.join(os.path.dirname(__file__), "..", "data", "B1", "CV_RMSE.png")
        if os.path.exists(image_path_RMSE):
            rmse_plot = Image.open(image_path_RMSE)
            st.image(rmse_plot, caption="Average 5-Fold CV RMSE by Model", width = 550)
        else:
            st.error(f"Image not found: {image_path_RMSE}")
        

    with col2:
        image_path_MAE = os.path.join(os.path.dirname(__file__), "..", "data", "B1", "CV_MAE.png")
        if os.path.exists(image_path_MAE):
            mae_plot = Image.open(image_path_MAE)
            st.image(mae_plot, caption="Average 5-Fold CV MAE by Model", width = 550)
        else:
            st.error(f"Image not found: {image_path_MAE}")

    st.markdown("### Model Conclusion")

    st.markdown("""
    From the performance plots above, we observe that the **Random Forest Regressor** consistently achieves the **lowest RMSE and MAE** across 5-fold cross-validation.

    This suggests that Random Forest outperforms other models not only by achieving lower prediction errors, but also by effectively capturing complex, nonlinear relationships between attraction demand and diverse external factors such as weather, events, and seasonality.

    ---
    **Final Choice:**  
    We conclude that the **Random Forest Regressor** is our most effective model and will be used to **predict the demand score** for each attraction.
    """)

    st.success("Random Forest selected as final predictive model based on overall performance.")


# ------------------ Page: Business Insights ------------------
elif page == "Business Insights":
    st.title("📊 Business Insights from Model Output")
    st.markdown("### Key Findings")

    # Feature importance image
    image_path_feature_imp = os.path.join(os.path.dirname(__file__), "..", "data", "B1", "feature_imp.png")
    if os.path.exists(image_path_feature_imp):
        feature_imp_plot = Image.open(image_path_feature_imp)
        st.image(feature_imp_plot, caption="Top 10 Feature Importances (Random Forest)", width = 700)
    else:
        st.error(f"Image not found: {image_path_feature_imp}")

    st.markdown("""
    - The **Log Flume**, **Merry-Go-Round**, and **Dizzy Dropper** attractions emerged as the top three predictors of attraction demand, ranking above weather-related factors like nearby cyclone risks and rain.
    - This suggests that **inherent ride appeal outweighs adverse weather conditions** in influencing attraction demand.
    - A possible implication is that visitors **may still be drawn** to these rides despite bad weather.
    - **Recommendations:**
        - Enhance or expand these high-appeal rides to boost demand.
        - Add **sheltered infrastructure** around key attractions to buffer the impact of adverse weather.
    """)

    


# ------------------ Page: Limitations ------------------
elif page == "Limitations & Improvements":
    st.title("⚠️ Limitations & Improvements")
    st.markdown("### Key Limitations & Business-Centered Improvements")

    st.markdown("""
    - **Limited Ground Truth on Demand:**  
      The demand score is a derived metric—based on scaled wait times and total visitor count—but may not fully reflect true customer intent or satisfaction. For example, high wait times may result from staffing issues rather than actual popularity.

      ➤ *To improve business accuracy, future models should incorporate direct demand signals such as ticket scans, ride entry counts, or mobile tracking data. These would better represent actual visitor choices and attraction popularity.*

    ---

    
    - **Model Interpretability vs. Complexity:**  
      Random Forests, while highly accurate, operate as black-box models—making it difficult for non-technical stakeholders to understand or trust the predictions.

      ➤ *From a decision-making perspective, applying explainability tools such as SHAP or LIME can help park managers to more precisely understand why certain variables drive demand. This makes insights more actionable as it helps to align model outputs with business strategies more effectively.*
    """)

    st.info("Linking model limitations to practical improvements ensures the predictive model remains valuable, explainable, and operationally useful for theme park decision-making.")