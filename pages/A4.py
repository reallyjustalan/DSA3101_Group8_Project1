import streamlit as st
<<<<<<< HEAD
=======
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import STL
from scripts.A4.s08_kmeans_pca import plot_clusters, get_dendrogram
from scripts.A4.s05_analysis_attendees import get_STL_decomposition
from scripts.A4.s06_analysis_avg_crowd import get_lift_of_campaign, df_crowd
from scripts.A4.s12_retail_modelling import determine_optimal_k, plot_3d_clusters, get_kmeans_labels
>>>>>>> b276a49389d5e784e2406c77db9c92c18ecb418f

# Configure page
st.set_page_config(
    page_title="Marketing Impact on Guest Behaviour",
    page_icon="🎢",
    layout="wide"
)

<<<<<<< HEAD
import s03_marketing_clustering as s03
import s06_retail_modelling as s06
=======
# Load data
@st.cache_data
def load_data():
    attendee_df = pd.read_csv('data/A4/raw/attendee.csv')
    crowd_df = pd.read_csv('data/A4/raw/avg_crowd.csv')
    crowd_df['date'] = pd.to_datetime(crowd_df['year'].astype(str) + '-' + crowd_df['month'], format='%Y-%b')
    return attendee_df, crowd_df

attendee_df, crowd_df = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Theme Park Analytics", "Campaign Analysis", "Customer Segmentation"])

# Theme Park Analytics Page
if page == "Theme Park Analytics":
    st.title("🎢 Theme Park Performance Analytics")
>>>>>>> b276a49389d5e784e2406c77db9c92c18ecb418f
    
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
        df = pd.read_csv('data/A4/clean/rmf.csv')
        determine_optimal_k(df.iloc[:,1:])  # Using function from s12_retail_modelling
        st.pyplot(plt.gcf())
    
    if st.button("Generate Customer Segments"):
        st.write("### 3D Visualization of Customer Segments")
        df = pd.read_csv('data/A4/clean/rmf.csv')
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
<<<<<<< HEAD
""", unsafe_allow_html=True)

# Create three boxed items
with st.container():
    # Item 1
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown('<div class="item-box">Know your customer</div>', unsafe_allow_html=True)        
    with col2:
        st.markdown('<div class="header">Who are they? What do they really want?</div>', unsafe_allow_html=True)
    
    # Item 2
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown('<div class="item-box">Communicate value clearly</div>', unsafe_allow_html=True)        
    with col2:
        st.markdown('<div class="header">No jargon, no fluff—just a straightforward promise.</div>', unsafe_allow_html=True)
        
    # Item 3
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown('<div class="item-box">Utilizing right channels</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="header">Fish where the fish are. If your customers are on Facebook, don\'t waste money on billboards.</div>', unsafe_allow_html=True)

mini_para_break()

st.markdown(
"""<p style='font-size:24px; color:white;'>
While many enthusiasts and experts offer their perspectives, we will be
offering a two-prong approach for your company to increase revenue through 
sales.</p>       
""", 
unsafe_allow_html=True)

st.divider()

st.markdown(
f"""<h3 class='subheading'>
Campaign Clustering: Key Findings
</h1>
""",unsafe_allow_html=True)

st.markdown(
"""<p style='font-size:24px; color:white;'>
Lower monthly crowd levels in theme parks are coupled with good marketing 
outcomes. Furthermore, campaigns from Disney performed best.  
</p>       
""", 
unsafe_allow_html=True)
mini_para_break()
st.markdown(
f"""<h3 class='subheading'>
Campaign Clustering: Motivation
</h1>
""",unsafe_allow_html=True)

st.markdown(
"""<p style='font-size:24px; color:white;'>
We will be using raw data webscraped from https://queue-times.com/. As of 01 
April 2025, the website offers various monthly and yearly information about 
theme parks for each year. We will be focusing on the label monthly crowd levels
to measure visitor rates to theme parks of interest. To standardize the analysis,
campaigns across theme parks around the world after the peak of covid had been 
identified, particularly campaigns after 2023. For the purpose of this analysis,
we are strictly looking at the numbers and ignoring qualitative factors like how
influenced a guest is to a campaign as those are more abstract in measuring. 
Solely by looking at the numbers, we can still draw useful insights. </p>       
""", 
unsafe_allow_html=True)

mini_para_break()

st.markdown(f"<h3 class='subheading'>Campaign Clustering: Measurement</h1>",
            unsafe_allow_html=True)

st.markdown(
"""<p style='font-size:24px; color:white;'>
The monthly crowd levels one month before and after each campaigns were identified.
We wanted to find out if more guests were visiting theme parks after campaigns, 
therefore we calculated the absolute and percentage increase in monthly crowd levels
before and after campaigns. However, the increase in crowd levels could also be 
attributed to seasonal effects. For example, it is known for summer holidays 
(June-August) to be the most crowded months in Singapore's Universal Studios. A 
campaign during those periods might not have great effect on guest decisions. Therefore,
we obtained the average monthly post-covid crowd levels in the years before the 
campaign to account for this seasonality effect.</p>""",
unsafe_allow_html=True)

mini_para_break()

st.markdown(
"""<p style='font-size:24px; color:white;'>
Determinants of campaign effect now consists of... </p>
""",
unsafe_allow_html=True)
st.markdown("""
<div style='font-size:24px; color:white;'>
  <div><b><em>Absolute Marketing Lift</b></em>: absolute increase one month post campaigns, accounting for seasonality</div>
  <div><b><em>Percentage Marketing Lift</b></em>: percentage increase one month post campaigns, accounting for seasonality</div>
  <div><b><em>Average Crowd Level</b></em>: crowd level the month before the campaign</div>
</div>
""", unsafe_allow_html=True)

mini_para_break()

st.markdown(f"<h3 class='subheading'>Campaign Clustering: Findings</h1>",
            unsafe_allow_html=True)

st.markdown("""<p style='font-size:24px; color:white;'>            
By performing similarity analysis using KMeans algorithm and PCA to visualize 
the clusters, we have distinguished the good campaigns from the bad campaigns as
seen from the red and green clusters in <a href="#figure1"> Figure 1</a>. 
</p>  
""", unsafe_allow_html=True)

st.markdown('<a name="figure1"></a>', unsafe_allow_html=True)  # Anchor
mini_para_break()
fig, ax, components,vars = s03.get_clusters(s03.campaign_df)
PCA1, PCA2 = components[0], components[1]
X1,X2,X3 = '(CrowdLevel)', '(AbsLift)', '(RelLift)'
st.pyplot(fig)




# set anchor for cross referencing
st.markdown('<a name="mathref1"></a>', unsafe_allow_html=True) 
mini_para_break()
 # Anchor
st.latex(fr"""
\begin{{aligned}}
PC_1 &= {PCA1[0]} \times \text{X1} + {PCA1[1]} \times \text{X2} + {PCA1[2]} \times \text{X3} \\
PC_2 &= {PCA2[0]} \times \text{X1} + {PCA2[1]} \times \text{X2} +  {PCA2[2]} \times \text{X3} \\

\mathrm{{Var}}_{{(PC_1)}} &= {vars[0]} \\
\mathrm{{Var}}_{{(PC_2)}} &= {vars[1]}  

\end{{aligned}}
""")
mini_para_break()

st.markdown("""<p style='font-size:24px; color:white;'>         
Since the <a href="#mathref1">explained variance of the first principle component
</a> is very close to 1, it tells us that the first principle component would
give us the most insight to exploring the relationship between clusters and the
features. Specifically, we can see from the x-axis in <a href="#figure1">Figure 
1</a> that more negative values (below -0.5) are an indicator of bad marketing
campaigns, while higher values (above -0.5) lead to better marketing campaigns.
</p>
""",unsafe_allow_html=True)
mini_para_break()
st.markdown(
"""<p style='font-size:24px; color:white;'> 
From <a href="#mathref1">PC_1's equation</a>, can deduce that higer marketing 
lifts (absolute/relative lifts) and lower monthly average crowd levels the month
before campaigns are an indication of better marketing, vice versa. 
</p>
""", unsafe_allow_html=True)

st.divider()
st.markdown(f"<h3 class='subheading'>Marketing Guest Segmentation: Key Findings</h1>",
            unsafe_allow_html=True)
st.markdown(
"""<p style='font-size:24px; color:white;'> 
Online shopping customers can be easily categorized into subgroups. For this 
dataset worked with, the categories range from new customers to premium 
customers.   
</p>
""", unsafe_allow_html=True)

mini_para_break()
st.markdown(f"<h3 class='subheading'>Marketing Guest Segmentation: Motivation</h1>",
            unsafe_allow_html=True)
st.markdown(
"""<p style='font-size:24px; color:white;'> 
In order to get good marketing, it is paramount to understand the pool of guests 
for any given company. If we are able to categorize guests into appropriate 
groups, we can have targetted marketing for each segment.
</p>
""", unsafe_allow_html=True)

mini_para_break()
st.markdown(
"""<p style='font-size:24px; color:white;'> 
Getting any form of data from visitors in theme parks are very scarce. Therefore,
an adjacent industry will be analyzed. Customers in adjacent industry has to 
fulfil the following characteristics that mimics the qualities of theme park 
revenues:  <b><em>presence of transactional sales; repetition of transactions
</b></em></p>
""", unsafe_allow_html=True)

mini_para_break()

st.markdown(
"""<p style='font-size:24px; color:white;'> 
The online retail industry meets these characteristics since customers purchase
their products (similar to purchasing a ticket), and some customers purchase 
their products in different periods of time (similar to a customer purchasing 
tickets once a year to visit a theme park). Therefore, a 2011 dataset on a 
registered small online retail company in UK from Dec 2010 to Dec 2011. 
</p>
""", unsafe_allow_html=True)

mini_para_break()
st.markdown(f"<h3 class='subheading'>Marketing Guest Segmentation: Measurement</h1>",
            unsafe_allow_html=True)
st.markdown(
"""<p style='font-size:24px; color:white;'> 
We will be employing Recency Frequency Monetary framework (RFM) to characterize 
all customers. 
</p>
""", unsafe_allow_html=True)
mini_para_break()
st.markdown("""
<div style='font-size:24px; color:white;'>
  <div><b><em>Recency</b></em>: Number of days since last purchase</div>
  <div><b><em>Frequency</b></em>: Total number of unique transactions</div>
  <div><b><em>Monetary</b></em>: Total amount spent in purchases</div>
</div>
""", unsafe_allow_html=True)

mini_para_break()
st.markdown(
"""<p style='font-size:24px; color:white;'> 
Using this framework, we can determine the type of customers exists in the 
company. For instance, if a customer made a recent high value purchase, and 
frequently purchases items from a company, they are (more or less) considered 
premium customers. Through such categorization, companies can apply targetted 
advertising to each customer segment. The number of groups that exists for this
dataset was determined using the 'elbow' method, for which is 4 clusters. 
</p>
""", unsafe_allow_html=True)

st.write(s06.df_labelled['Segment'].value_counts().rename('Total number of customers'))


mini_para_break()

st.markdown(f"<h3 class='subheading'>Marketing Guest Segmentation: Findings</h1>",
            unsafe_allow_html=True)
st.markdown(
"""<p style='font-size:24px; color:white;'> 
<a href='#figure2'>Figure 2</a> shows us how customers are segmented in their 
clusters according to recency, frequency, and monetary features. 
<a href='#table1'>Table 1</a> shows us the ranks for each customer segment 
with reference to the RMF framework. 'Champion' customers have the highest 
frequency, monetary, and recency. 'At Risk' customers have the second
highest frequency, monetary, but the third highest recency. 'Potential 
Loyalists' customers have the third highest frequency, monetary, but second 
highest recency. Finally, 'New Customers' is ranked last across all features in
the framework.
</p>
""", unsafe_allow_html=True)
mini_para_break()

st.markdown('<a name="table1"></a>', unsafe_allow_html=True)  # Anchor
st.markdown("""
**Table 1: Customer Cluster Rankings**

| Segment | Frequency_Rank | Monetary_Rank | Recency_Rank |
|---------------------|-------|---------|-------|
| Champions           | 1    |1     | 1   |
| At Risk             | 2    |2     | 3*    |
| Potential Loyalists | 3    |3     | 2*    |
| Hiberting       | 4    |4     | 4    |
""")

st.markdown('<a name="figure2"></a>', unsafe_allow_html=True)  # Anchor
fig= s06.plot_3d_clusters(s06.df_labelled) 
st.plotly_chart(fig)


st.markdown(f"<h3 class='subheading'>Marketing Guest Segmentation: Tailored Marketing</h3>",
            unsafe_allow_html=True)
st.markdown(f"<h5 class='subsubheading'>Champions</h5>",
            unsafe_allow_html=True)
st.markdown(
"""<p style='font-size:24px; color:white;'> 
These customers have the highest rank in the whole RFM framework, this indicates
that they are recently making high-value transactions frequently. Therefore, 
the company can offer exclusive VIP reward programs with tiered benefits to 
encourage more spending via tokens of appreciation. 
</p>
""", unsafe_allow_html=True)


st.write("")
st.markdown(f"<h5 class='subsubheading'>At Risk</h5>",
            unsafe_allow_html=True)
st.markdown(
"""<p style='font-size:24px; color:white;'> 
These customers have the next highest rank in frequency and monetary, but comes
in third rank in recency. These customers are similar to 'Champion' customers 
except that they have not been recently been shopping on the company's online 
platform. Therefore, the company can offer can tap into "We miss you" 
time-sensitive discounts. Furthermore, companies can also increase advertisement
towards subscriptions with first month discount to entice customers to subscribe
while providing the company with recurring revenue per 'At Risk' customers. 
</p>
""", unsafe_allow_html=True)

st.write("")
st.markdown(f"<h5 class='subsubheading'>Potential Loyalists</h5>",
            unsafe_allow_html=True)
st.markdown(
"""<p style='font-size:24px; color:white;'> 
These customers have the third highest rank in frequency and monetary, but comes
in second rank in recency. These customers have shown interest in the companies
products but have not spent the most in them nor made many transactions with the
company. To promote greater interest in company products, the company can 
possibly focus on customer-centric marketing approach by including how-to 
guides, which would enhance the post-purchase experience, possibly leaving a 
better impression on customers, therefore encouraging future purchases and 
recommendation to their friends and families. In addition, companies can include
time-locked offers exclusively for recent customers such as "2-for-1 ends soon"
slogan their products, potentially increasing the total amount spent on company
products.  
</p>
""", unsafe_allow_html=True)

st.write("")
st.markdown(f"<h5 class='subsubheading'>Hibernating</h5>",
            unsafe_allow_html=True)
st.markdown(
"""<p style='font-size:24px; color:white;'> 
'Hibernating' customers come in last ranked across the RMF framework. They are
inactive, making low-value purchase and not often. This could be a result of 
discontent with company product. Therefore, the company could tap into 
feedback-based marketing where the company obtain customer sentiment as well as
pain points, and to reward for their time, they get exclusive discount coupons 
for their next purchase. In addition, the company can include low-cut 
touchpoints for these users, such as free subscription to company newsletters 
showcasing new product listings. Lastly, to draw savings-based attention towards
customers, the company can leverage on reactivation-based marketing, offering
"We want you back" exclusive discounts to such customers.
 
</p>
""", unsafe_allow_html=True)




references = ['https://www.statista.com/statistics/286526/coca-cola-advertising-spending-worldwide/',]
=======
""", unsafe_allow_html=True)
>>>>>>> b276a49389d5e784e2406c77db9c92c18ecb418f
