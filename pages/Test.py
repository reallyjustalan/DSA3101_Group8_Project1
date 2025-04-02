import streamlit as st
import sys
from pathlib import Path
# Add the directory containing vis_1.py to the Python path
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
    ### How can IoT technology improve guest experience in theme parks?
    """
)

# Title of the app
st.title("Crowd Analysis using WiFi signal data")

# Sidebar for navigation using st.radio
navigation = st.sidebar.radio("Navigation", ["Overview", "1) Geography", 
                                             "2) Exploratory Data Analysis", "3) Modelling"])


if navigation == "Overview": # Overview Section
    st.markdown(
        """
        # Placeholder"""
    )
if navigation == "1) Geography": # Geographical plots (Interactive)
    st.header("Welcome to the Home Page")
    st.write("This is the home page of the dashboard.")
    left, right = st.columns(2)

    # Initialize session state for button and sliders
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
            "<h2 style='text-align: center; font-size: 24px;'>3D scatterplot of geographical layout.</h2>",
            unsafe_allow_html=True
        )

        # Update the plot dynamically
        fig, ax = plot3d()
        ax.view_init(elev=st.session_state.elevation, azim=st.session_state.azimuth)
        st.pyplot(fig, clear_figure=True)

        # Create sliders for azimuth and elevation
        st.session_state.azimuth = st.slider("Azimuth", 180, 360, st.session_state.azimuth)
        st.session_state.elevation = st.slider("Elevation", 0, 90, st.session_state.elevation)
    

if navigation == "2) Exploratory Data Analysis": # EDA section

    st.write("In this section we will explore the data to identify the trends and "
    "distributions of selected parameters.")

    # Create columns for buttons
    left, right = st.columns(2)

    # Initialize session state for button and sliders
    if "button_pressed" not in st.session_state:
        st.session_state.button_pressed = None

    # WAP barplot button
    if left.button("Exploratory Analysis", use_container_width = True):
        st.session_state.button_pressed = "Exploratory Analysis"

    # HeatMap & crowd movement trends
    if right.button("Crowd Density", use_container_width = True):
         st.session_state.button_pressed = "Crowd Density"

    # if WAP button pressed
    if st.session_state.button_pressed == "Exploratory Analysis":
        
        st.write("Here we aim to visualise the data to help decide how to train the model.\n")
        # st.header("Visitor Flow Network")
        st.header("WiFi Access Point Distribution")
        
        # Barplot of the number of WAPs on each floor in each building
        fig3, ax3 = wap_distrubution()
        st.pyplot(fig3, clear_figure=True)

        st.write("This plot reveals that the variance of WAPs is the smallest in building 0 "
        "and on floor 2. Therefore, we will train and test our model on predicting crowds in "
        "building 0 and across all buildings on floor 2.")

        st.header("Number of unique users per day")

        fig4, ax4 = user_plot()
        st.pyplot(fig4, clear_figure=True)

        st.write("From this, we can tell that there are users who consistently visit "
        "building 0 before and after '2013-06-20'. This makes building "
        "0 a more viable option for training our model as it has less bias.\nThe barplot also shows an "
        "explosive increase of users visiting building 1 and 2 on '2013-06-20'.")

    # If heatmap button pressed
    if st.session_state.button_pressed == "Crowd Density":

        st.write("Here we visualise crowd density with a combination of "
        "heatmaps and scatterplots")

        # Initialise tabs
        tab1, tab2 = st.tabs(["No Trend", "Trend"])
        
        with tab1:

            st.write("Contour map of crowd density, highlighting the most crowded areas.\n")
            fig5, ax5 = create_heatmap()
            st.pyplot(fig5, clear_figure = True)

        with tab2:
            st.write("Spatial map of crowd density with a trendline that shows how the crowd moves.\n")
            fig6, ax6 = create_heatmap_trend()
            st.pyplot(fig6, clear_figure = True)


if navigation == "3) Modelling": # Modelling Section
    st.write("In this section we will train models to predict the location of individuals. "
    "But the focus is getting an idea of the crowd distribution so we do not scrutinize "
    "the precision of individual locations.")

    # Create columns for buttons
    left, right = st.columns(2)

    # Initialize session state for button and sliders
    if "model_button_pressed" not in st.session_state:
        st.session_state.model_button_pressed = None

    # 3D Model Metrics button
    if right.button("3D Model Metrics", use_container_width=True):
        st.session_state.model_button_pressed = "3D Model Metrics"
        
    # 2D Model Evaluation button
    if left.button("2D Model Metrics", use_container_width=True):
        st.session_state.model_button_pressed = "2D Model Metrics"

    # if 3D button pressed
    if st.session_state.model_button_pressed == "3D Model Metrics":
        st.write("Below is a model trained on WiFi signal strength to predict crowd "
        "densities within a given area.")
        
    # if 2D Model Metrics button pressed
    if st.session_state.model_button_pressed == "2D Model Metrics":
        st.header("Model Performance Evaluation")

        st.write("Below is a model trained on WiFi signal strength to predict crowd "
        "densities within a given area.")
    
        # Initialize tabs for different views
        tab1, tab2 = st.tabs(["Metrics Comparison", "Visual Diagnostics"])
        if 'results_df' not in st.session_state:
            st.session_state.results_df = None
        if 'all_figures' not in st.session_state:
            st.session_state.all_figures = {}
        with tab1:
            st.subheader("Model Performance Metrics")
            
            if st.session_state.results_df is not None:
                st.dataframe(st.session_state.results_df.style.format({
                    'MSE': '{:.4f}',
                    'R²': '{:.4f}',
                    'Adjusted R²': '{:.4f}'
                }))

            else:
                st.warning("No model results available. Please run evaluation first.")
            
            if st.button("Run Model Evaluation", key="eval_button"):
                with st.spinner("Evaluating models..."):
                    results_df, all_figures = evaluate_all_models(
                        loaded_models, X_test_new, y_test_reg_new, coord_scaler
                    )
                    st.session_state.results_df = results_df
                    st.session_state.all_figures = all_figures or {}  # Ensure it's never None
                st.success("Evaluation complete!")
                st.rerun()
        
        with tab2:
            st.subheader("Model Diagnostic Plots")
            
            # Check if we have figures and they're in the correct format
            if not st.session_state.all_figures or not isinstance(st.session_state.all_figures, dict):
                st.warning("Please run model evaluation first")
            else:
                model_choice = st.selectbox(
                    "Select Model to Inspect",
                    options=list(st.session_state.all_figures.keys())
                )
                
                figures = st.session_state.all_figures.get(model_choice, [])
                
                if not figures or len(figures) < 2:
                    st.error("Diagnostic plots not available for this model")
                else:
                    # Display combined residual plots
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