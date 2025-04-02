import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import STL
from scripts.A4.s08_kmeans_pca import plot_clusters, get_dendrogram
from scripts.A4.s06_analysis_avg_crowd import get_lift_of_campaign, df_crowd
from scripts.A4.s05_analysis_attendees import get_STL_decomposition
from scripts.A4.s12_retail_modelling import determine_optimal_k, plot_3d_clusters, get_kmeans_labels

# Configure page
st.set_page_config(
    page_title="Marketing Impact on Guest Behaviour",
    page_icon="🎢",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    attendee_df = pd.read_csv('data/A4/raw/attendee.csv')
    crowd_df = pd.read_csv('.data/A4/raw/avg_crowd.csv')
    crowd_df['date'] = pd.to_datetime(crowd_df['year'].astype(str) + '-' + crowd_df['month'], format='%Y-%b')
    return attendee_df, crowd_df

attendee_df, crowd_df = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Theme Park Analytics", "Campaign Analysis", "Customer Segmentation"])

# Theme Park Analytics Page
if page == "Theme Park Analytics":
    st.title("🎢 Theme Park Performance Analytics")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Filters")
        park = st.selectbox("Select Theme Park", crowd_df['name'].unique())
        start_date = st.date_input("Start Date", value=pd.to_datetime('2016-01-01'))
        end_date = st.date_input("End Date", value=pd.to_datetime('2024-12-31'))
        
        analysis_type = st.radio("Analysis Type", 
                               ["Time Series", "Seasonal Decomposition", "Moving Average"])
        
        if analysis_type == "Moving Average":
            window_size = st.slider("Moving Average Window Size", 3, 12, 3)
    
    with col2:
        st.subheader("Analysis Results")
        
        # Filter data based on selections
        filtered_df = crowd_df[
            (crowd_df['name'] == park) & 
            (crowd_df['date'] >= pd.to_datetime(start_date)) & 
            (crowd_df['date'] <= pd.to_datetime(end_date))
        ].sort_values('date')
        
        if not filtered_df.empty:
            if analysis_type == "Time Series":
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(filtered_df['date'], filtered_df['avg_crowd_level'])
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
                plt.xticks(rotation=45)
                ax.set_title(f'Average Crowd Level for {park}')
                ax.set_ylabel('Average Crowd Level (%)')
                st.pyplot(fig)
                
            elif analysis_type == "Seasonal Decomposition":
                st.write("### STL Decomposition")
                temp_df = filtered_df.set_index('date').dropna()
                ts = temp_df['avg_crowd_level']
                stl = STL(ts, period=12).fit()
                fig = stl.plot()
                plt.xticks(rotation=45)
                st.pyplot(fig)
                
            elif analysis_type == "Moving Average":
                fig, ax = plt.subplots(figsize=(10, 6))
                ts = filtered_df.set_index('date')['avg_crowd_level']
                sma = ts.rolling(window=window_size, center=True).mean()
                
                plt.plot(ts, label='Original Data', alpha=0.3)
                plt.plot(sma, label=f'Trend ({window_size}-MA)')
                plt.xlabel('Date')
                plt.ylabel('Avg Crowd Level (%)')
                plt.legend()
                plt.xticks(rotation=45)
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
                st.pyplot(fig)
        else:
            st.warning("No data available for the selected filters.")

# Campaign Analysis Page
elif page == "Campaign Analysis":
    st.title("📈 Marketing Campaign Impact Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Campaign Clustering")
        st.write("""
        Campaigns are clustered based on:
        - Average crowd during campaign month
        - Absolute lift in attendance
        - Percentage lift in attendance
        """)
        
        if st.button("Generate Campaign Clusters"):
            st.write("### K-Means Clustering (PCA Visualization)")
            plot_clusters(pd.DataFrame())  # Using the function from s08_kmeans_pca
            st.pyplot(plt.gcf())
    
    with col2:
        st.subheader("Campaign Hierarchy")
        st.write("""
        Dendrogram showing hierarchical clustering of campaigns based on performance metrics.
        """)
        if st.button("Generate Dendrogram"):
            st.write("### Hierarchical Clustering Dendrogram")
            fig, ax = get_dendrogram(pd.DataFrame())  # Using the function from s08_kmeans_pca
            st.pyplot(fig)
    
    st.subheader("Campaign Lift Calculator")
    park = st.selectbox("Select Theme Park", crowd_df['name'].unique())
    campaign_date = st.date_input("Campaign Start Date")
    campaign_name = st.text_input("Campaign Name")
    
    if st.button("Calculate Campaign Impact"):
        abs_lift, perc_lift, avg_crowd = get_lift_of_campaign(
            crowd_df, 
            park, 
            campaign_date.strftime('%Y-%m-%d'), 
            campaign_name
        )
        
        st.metric("Average Crowd During Campaign Month", f"{avg_crowd:.1f}%")
        st.metric("Absolute Lift After Campaign", f"{abs_lift:.1f} percentage points")
        st.metric("Percentage Lift After Campaign", f"{perc_lift:.1f}%")

# Customer Segmentation Page
elif page == "Customer Segmentation":
    st.title("👥 Customer Segmentation Analysis")
    
    st.write("""
    Customer segmentation using RFM (Recency, Frequency, Monetary) analysis 
    and K-Means clustering.
    """)
    
    if st.button("Determine Optimal Number of Clusters"):
        st.write("### Elbow Method for Optimal K")
        df = pd.read_csv('../data/clean/rmf.csv')
        determine_optimal_k(df.iloc[:,1:])  # Using function from s12_retail_modelling
        st.pyplot(plt.gcf())
    
    if st.button("Generate Customer Segments"):
        st.write("### 3D Visualization of Customer Segments")
        df = pd.read_csv('../data/clean/rmf.csv')
        df_labelled = get_kmeans_labels(df.iloc[:,1:])
        df_labelled['CustomerID'] = df['CustomerID']
        plot_3d_clusters(df_labelled)
        st.plotly_chart(plt.gcf(), use_container_width=True)
        
        st.write("### Segment Characteristics")
        segments = df_labelled.groupby('Segment').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean'
        }).reset_index()
        st.dataframe(segments.style.format({
            'Recency': '{:.1f}',
            'Frequency': '{:.1f}',
            'Monetary': '{:.1f}'
        }))

# Add some styling
st.markdown("""
<style>
    .stMetric {
        border-left: 5px solid #4CAF50;
        padding: 10px;
        background-color: #f9f9f9;
        border-radius: 5px;
    }
    .css-1aumxhk {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)