import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'scripts' / 'B5'))
from vis_1_2 import *
from vis_3 import wap_distrubution
from vis_4 import user_plot
from vis_5 import create_heatmap
from vis_6 import create_heatmap_trend
from trained_models_1 import *
from ml_1 import *

st.markdown(
    """
    # B5
    # How can IoT technology improve guest experience in theme parks?
    """
)

# Sidebar for navigation using st.radio
navigation = st.sidebar.radio("Navigation", ["Overview", "1) Geography", 
                                             "2) Exploratory Data Analysis", 
                                             "3) Modelling", "Conclusion"])


if navigation == "Overview": # Overview Section

    st.markdown("""
    ## **Overview of WiFi-Based Crowd Analysis**
    This project explores the use of WiFi signal strength for crowd analysis by 
                predicting the longitude and latitude of individuals within a defined 
                indoor space. By leveraging a dataset of WiFi Access Point (WAP) signals, 
                the goal is to train a machine learning model that is capable of estimating the 
                locations of people based on the received signal strength from multiple 
                access points. 

    ## **Motivation**
    In theme parks, accurate crowd analysis is essential for a smooth and enjoyable 
                guest experience. Traditional methods of crowd management, 
                are labor-intensive and inefficient. WiFi-based localization enables 
                theme park operators can gain real-time insights on crowd densities and 
                how crowds are moving throughout the park. This data can help predict 
                crowd behavior, improve decision-making, and enhance safety.

    ## **Methodology**""")
    with st.expander("### 1. **Data Preprocessing**"):
        st.markdown("""
    - The dataset contains WiFi signal strengths recorded from 520 WAPs, along with longitude, 
                    and latitude.
    - Signals range from -104 (weakest) to 0 (strongest), with 100 indicating no detection.  
    - The data is filtered based on `BUILDINGID` to analyze specific buildings separately.  
    - The dataset is split into training and test sets based on date (`DATE < '2013-07-20'` for 
                    training and `DATE > '2013-07-20'` for testing).
    - These dates are chosen referencing the training and validation data sets.  
    - Features are preprocessed using scaling, selection, and encoding techniques.  
    - Target coordinates are scaled using `StandardScaler` for regression models, 
                    while categorical labels (such as floor levels) are encoded using `LabelEncoder`.""")  

    with st.expander("### 2. **Feature Engineering**"):
           st.markdown("""
    - Selecting relevant WAPs with strong signals.  
    - Transforming signal strength data into meaningful location features using feature 
                       selection methods.""")  

    with st.expander("### 3. **Model Selection & Training**"):
           st.markdown("""
    - Various regression models are trained to predict longitude and latitude, including:
    - **XGBoost** (boosted decision trees)
    - **Gradient Boosting**
    - **Random Forest**
    - **Support Vector Regression (SVR)**
    - **Multi-layer Perceptron (MLP)**
    - Models are trained using preprocessed data, with training and validation splits (80/20).  
    - Trained models are saved for future evaluation.""")

    with st.expander("### 4. **Evaluation & Visualization**"):
           st.markdown("""
    - Models are evaluated based on **Mean Squared Error (MSE)**, **R² Score**, 
                       and **Adjusted R² Score**.
    - Predictions are compared with actual coordinates using scatter plots.
    - Trained models are loaded and tested on unseen data to assess generalization ability.""")

    st.markdown("""              
    ## **Expected Outcomes**
    - A  model that predicts a person’s location based on WiFi signals.  
    - Insights into crowd density across a given layout.  
    - Potential applications for real-time crowd monitoring and space optimization.  
    """)


    
if navigation == "1) Geography": # Geographical plots (Interactive 3D)
    st.markdown("""
        ## **Geography**
        In the **Geography** section, we visualised the indoor layout using WiFi signal data. 
                A static 2D and an interactive 3D plot allow users to explore the physical 
                layout of the buildings. The view of the 3D plot can be adjusted via the azimuth 
                and elevation sliders which provides a dynamic view of the environment.
""")
    left, right = st.columns(2)

    # Initialize session state for button and sliders
    # Session state prevents the webpage from refreshing everytime user interacts with it
    if "button_pressed" not in st.session_state:
        st.session_state.button_pressed = None
    if "azimuth" not in st.session_state:
        st.session_state.azimuth = 270
    if "elevation" not in st.session_state:
        st.session_state.elevation = 12
    
    # 2D-Plot button
    if left.button("2D-Plot", use_container_width=True):
        st.session_state.button_pressed = "2D-Plot"
    
    # 3D-Plot button
    if right.button("3D-Plot", use_container_width=True):
        st.session_state.button_pressed = "3D-Plot"
    
    # Display the selected plot
    if st.session_state.button_pressed == "2D-Plot":
        st.markdown(
            "<h2 style='text-align: center; font-size: 24px;'>2D scatterplot of geographical layout.</h2>",
            unsafe_allow_html=True
        )
        fig2, ax2 = scatter()
        st.pyplot(fig2)

    elif st.session_state.button_pressed == "3D-Plot":
        st.markdown(
            "<h2 style='text-align: center; font-size: 24px;'> Interactive 3D scatterplot of geographical layout.</h2>",
            unsafe_allow_html=True
        )

        # Update the plot dynamically
        fig, ax = plot3d()
        ax.view_init(elev=st.session_state.elevation, azim=st.session_state.azimuth)
        st.pyplot(fig, clear_figure=True)

        # Create sliders for azimuth and elevation
        st.session_state.azimuth = st.slider("Azimuth", 180, 360, st.session_state.azimuth)
        st.session_state.elevation = st.slider("Elevation", 0, 90, st.session_state.elevation)
        st.rerun()
    

if navigation == "2) Exploratory Data Analysis": # EDA section

    st.markdown("""
            ## **Exploratory Data Analysis (EDA)**
            The **EDA** section expounds upon the elements of the dataset to uncover hidden 
                trends and patterns. First we analyse the distribution of number of entries 
                across different floors and buildings. Next, a barplot of unique users per day 
                shows an explosive increase in the number of visitors to buildings 1 and 2 on 
                '2013-06-20' suggesting an event that influences crowd behavior occured.
                Spatial heatmaps help visualise and examine crowd density. Understanding the layout 
                is essential for theme park organisers as it enables key stakeholders to 
                communicate more effectively and make informed decisions.
""")

    # Create columns for buttons
    left, right = st.columns(2)

    # Initialize session state for button and sliders
    if "button_pressed" not in st.session_state:
        st.session_state.button_pressed = None

    # Left barplot button
    if left.button("Exploratory Analysis", use_container_width = True):
        st.session_state.button_pressed = "Exploratory Analysis"

    # HeatMap & crowd movement trends
    if right.button("Crowd Density", use_container_width = True):
         st.session_state.button_pressed = "Crowd Density"

    # if Left button pressed
    if st.session_state.button_pressed == "Exploratory Analysis":
        
        st.write("Here we aim to visualise the data to help decide how to train the model.\n")
        st.header("Distribution of Data")
        
        # Barplot of the number of data entries on each floor in each building
        fig3, ax3 = wap_distrubution()
        st.pyplot(fig3, clear_figure=True)

        st.write("This plot reveals that the number of data entries is the most even in building 0 "
        "and on floor 2. Therefore, we will train and test our model on predicting crowds in "
        "building 0 and across all buildings on floor 2. Therefore, it would serve as a good "
        "starting point for visualing and modelling.")

        st.header("Number of unique users per day")
        # Barplot of number of unique users
        fig4, ax4 = user_plot()
        st.pyplot(fig4, clear_figure=True)

        st.write("From this, we can tell that there are users who consistently visit "
        "building 0 before and after '2013-06-20'. This makes building "
        "0 a more viable option for training our model as it has less bias.\nThe barplot also shows an "
        "explosive increase of users visiting building 1 and 2 on '2013-06-20'. This suggests "
        "that there may be some kind of event or grand opening of buildings 1 and 2")

    # If heatmap button pressed
    if st.session_state.button_pressed == "Crowd Density":

        st.write("Here we visualise crowd density with a combination of "
        "heatmaps and scatterplots")

        # Initialise tabs
        tab1, tab2 = st.tabs(["No Trend", "Trend"])
        
        with tab1: # Heatmap with no trendline

            st.write("Spatial Heatmap of crowd density, highlighting the most crowded areas.\n")
            fig5, ax5 = create_heatmap()
            st.pyplot(fig5, clear_figure = True)
            st.write("This plot shows us the the locations of hot spots over a given period of time. "
            "This crucial information can assist theme parks in identifying crowded areas and "
            "deploy resources accordingly.")

        with tab2:# Heatmap with trendline

            st.write("Spatial Heatmap of crowd density with trendline.\n")
            fig6, ax6 = create_heatmap_trend()
            st.pyplot(fig6, clear_figure = True)
            st.write("This plot shows the area that crowds tend to gravitate towards. In a theme "
            "park envrionment, this could extremely useful as organisers will be able to better "
            "assign resources for more efficient operations and safety management.")

if navigation == "3) Modelling": # Modelling Section
    st.markdown("""
        ## **Modelling**
        In the **Modelling** section, we train various regression models to predict 
                crowd densities based on WiFi signal strength. These models were evaluated 
                using R² scores, Mean Squared Error (MSE), and Adjusted R² as performance 
                matrices. The models were primarily focused on predicting general crowd 
                distributions rather than individual locations. Residual plots and actual vs 
                predicted plots provide visual insights into model performance. The model 
                evaluation lets users compare the performance of the different models in 
                estimating crowd densities.

        ### **Model Performance Evaluation**
        * Please run the evaluation again if output is blank.
""")
    
    # Initialize tabs for different views
    tab1, tab2 = st.tabs(["Metrics Comparison", "Visual Diagnostics"])
    if 'results_df' not in st.session_state:
        st.session_state.results_df = None

    if 'all_figures' not in st.session_state:
        st.session_state.all_figures = {}

    with tab1: # Model Metrics Comparison
        st.subheader("Model Performance Metrics")
            
        if st.session_state.results_df is not None:
            st.dataframe(st.session_state.results_df.style.format({
                'MSE': '{:.4f}',
                'R²': '{:.4f}',
                'Adjusted R²': '{:.4f}'
            })) # Output as a df

        else:
            st.warning("No model results available. Please run evaluation first.")
           
        if st.button("Run Model Evaluation", key="eval_button"): # Press to show data
            with st.spinner("Evaluating models..."):
                results_df, all_figures = evaluate_all_models(
                    loaded_models, X_test_new, y_test_reg_new, coord_scaler
                )
                st.session_state.results_df = results_df
                st.session_state.all_figures = all_figures or {}  # Ensure it's never None
            st.success("Evaluation complete!")
            st.rerun()
        
    with tab2: # Tab with plots
        st.subheader("Model Diagnostic Plots")
            
        # Check if we have figures and they're in the correct format
        if not st.session_state.all_figures or not isinstance(st.session_state.all_figures, dict):
            st.warning("Please run model evaluation first")
        else:
            model_choice = st.selectbox( # Dropdown menu to choose plot for corresponding model
                "Select Model to Inspect",
                options=list(st.session_state.all_figures.keys())
            )
                
            figures = st.session_state.all_figures.get(model_choice, [])
                
            if not figures or len(figures) < 2:
                st.error("Diagnostic plots not available for this model")
            else:
                # Display residual plots
                st.write(f"### {model_choice} Residual Analysis")
                try:
                    st.pyplot(figures[0], clear_figure=True)
                    st.caption("Left: Longitude Residuals | Right: Latitude Residuals")
                except Exception as e:
                    st.error(f"Could not display residual plots: {str(e)}")
                    
                # Display actual vs predicted plot
                st.write(f"### {model_choice} Actual vs Predicted")
                try:
                    st.pyplot(figures[1], clear_figure=True)
                except Exception as e:
                    st.error(f"Could not display actual vs predicted plot: {str(e)}")

if navigation == "Conclusion": # Conclusion
    st.markdown("""
        ## **Conclusion**""")
    with st.expander("### **Project Key Takeaways**"):
        st.markdown("""
- High validation accuracy (R² ≈ 0.98) shows strong initial model performance.
- Low performance on unseen data (R² ≈ 0.25) suggests overfitting and generalization challenges.
- Models predicts rough crowd distribution, despite reduced accuracy.
- Visualizations provided valuable insights into:
    - Crowd densities
    - User movement patterns
    - Visitor anomalies
- Geographical and contour plots effectively illustrated spatial distributions.
- Spike in visits on 2013-06-20 indicates potential for event detection.
- Applications in theme parks include:
    - Better crowd management
    - Enhancing guest experience by guiding them to less crowded areas
- Future improvements:
    - Feature engineering & data augmentation
    - Advanced models (e.g., deep learning, hybrid approaches)
    - Incorporating temporal and weather data
- Strong foundation for future research in WiFi-based localization and crowd analytics.""")
    with st.expander("### **Full Conclusion**"):
        st.markdown("""
        The project demonstrates the potential of WiFi signal strength for
                 crowd analysis to be used in theme parks. While the 
                models performed exceptionally well on the validation set 
                with **R² scores around 0.98**, their performance dropped significantly 
                on unseen data, with **R² scores around 0.25** which suggests potential 
                overfitting and highlights the challenges of generalizing 
                location predictions across different time periods. Even with 
                the decreased performance on unseen data, the models are able to 
                predict a rough distribution of crowds.

        Despite these limitations, the visualization of historical data provided 
                valuable insights into crowd densities, user movement patterns, 
                and anomalies in visitor numbers. Then, the geographical layout and contour 
                plots effectively illustrated spatial distributions, and finally, the spike in 
                user visits on **2013-06-20** suggests the potential for event detection 
                using WiFi data.

        These findings have clear applications and benefits for theme park operations, 
                including crowd management and improving guest experience by incentivising 
                guests to explore and spend more time in less crowded areas. 

        Future improvements could focus on feature engineering, additional data 
                augmentation techniques, and advanced modeling approaches such as 
                deep learning or hybrid models. Additionally, incorporating more 
                temporal and weather features could improve predictive accuracy. 
                Overall, this project provides a strong foundation for further 
                research into WiFi-based localization and crowd analytics and shows 
                potential in transforming how theme parks manage their crowds and guest experiences.
        """)
