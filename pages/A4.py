import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # Adds finalfinal_marketing/ to path
import scripts.A4.s03_marketing_clustering as s03
import scripts.A4.s06_retail_modelling as s06

import streamlit as st

st.set_page_config(
    page_title='Marketing in Theme Parks',
    page_icon = '🔥',
    layout ='wide',
    initial_sidebar_state='expanded'
)

def big_para_break():
    st.write("")  # Adds empty space
    st.write("")  # Adds more space
    st.write("")  # Adds empty space
    st.write("")  # Adds more space
    st.write("")  # Adds empty space
    st.write("")  # Adds more space
def mini_para_break():
    st.write("")  # Adds empty space
    st.write("")  # Adds more space
    st.write("")  # Adds empty space
    
# Header
st.title("🔥 Marketing in Theme Parks")
st.write("#### What campaign techniques can we use to increase the number of visitors in theme parks?")
st.badge('success!', icon=':material/done_all:', color='blue')

# Create tabs instead of radio buttons
tab1, tab2, tab3 = st.tabs(["Overview", "Marketing Guest Segmentation","Campaign Clustering"])

with tab1:
    st.markdown(
    """<p style='font-size:20px; color:white;'>
    To an average Joe, marketing may seem like the simple task of posting a campaign alert on Facebook, or handing out 
    fliers promoting 20% discount at your nearby KBBQ restaurant. Unfortunately, this is not that simple. marketing is so 
    much more involved than advertising. In fact, we see big players in the drink industry such as Coca Cola pouring over
    $4.0 billion US dollars consistently for the past decade (with the exception of 2020 COVID-19 of course).</p>""", 
    unsafe_allow_html=True)

    st.markdown(
    """
    <p style='font-size:20px; color:white;'> In today's hyper-competitive marketplace, marketing is the cornerstone of 
    business success—a disciplined strategy that transforms products into brands, customers into advocates, and markets 
    into revenue streams. Marketing doesn't need to be complicated to be effective. At its core, it's about connecting the 
    right product with the right customer—clearly, efficiently, and profitably. While many enthusiasts and experts offer their perspectives, we will be
    offering a two-prong approach for your company to increase revenue through sales.</p>
    """,
    unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .item-box {
        font-weight: bold;
        font-size: 1.2em;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;  /* Vertical centering */
        justify-content: center;  /* Horizontal centering */
        text-align: center;  /* Fallback for text */
        min-height: 100px;  /* Minimum height for better visual */
    }
    .header {
        font-weight: bold;
        font-size: 1.1em;
        margin-bottom: 5px;
        padding: 30px;
        display: flex;
        align-items: center;
        padding-right: 15px;

    }
    </style>
    """, unsafe_allow_html=True)

    # Create three boxed items
    with st.container():
        # Item 1
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown('<div class="item-box">Know your customer</div>', unsafe_allow_html=True)        
        with col2:
            st.markdown('<div class="header">Who are they? What is their behavior?</div>', unsafe_allow_html=True)
        
        # Item 2
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown('<div class="item-box">Know your marketing</div>', unsafe_allow_html=True)        
        with col2:
            st.markdown('<div class="header">How well is your marketing performing?</div>', unsafe_allow_html=True)
    
    st.divider()
    
    left, _, right = st.columns([0.475, 0.05, 0.475])  # Middle column acts as a spacer

    with left:
        st.markdown(f"<h5 class='subheading'>Marketing Guest Segmentation</h5>",
                unsafe_allow_html=True)
        st.write(f"Go to 'Market Guest Segmentation' tab to find out more")
        
        fig= s06.plot_3d_clusters(s06.df_labelled) 
        st.plotly_chart(fig, key='Overview')
        
    with right:
        st.markdown(f"<h5 class='subheading'>Campaign Clustering</h5>",
                    unsafe_allow_html=True) 
        st.write(f"Go to 'Campaign Clustering' tab to find out more")
        fig, ax, components,vars = s03.get_clusters(s03.campaign_df)
        st.pyplot(fig)

with tab2:
    st.markdown(f"<h3 class='subheading'>Marketing Guest Segmentation: Key Findings</h1>",
                unsafe_allow_html=True)
    st.markdown(
    """<p style='font-size:20px; color:white;'> 
    Online shopping customers can be easily categorized into subgroups. For this 
    dataset worked with, the categories range from new customers to premium 
    customers. Similarly, theme park companies can perform guest segmentation
    to identify their types of customers and employ targetted marketing 
    strategies as explained later in <a href='#tailoredmarketting'> Tailored 
    Marketing section</a></p>
    """, unsafe_allow_html=True)

    mini_para_break()
    st.markdown(f"<h3 class='subheading'>Marketing Guest Segmentation: Motivation</h1>",
                unsafe_allow_html=True)
    st.markdown(
    """<p style='font-size:20px; color:white;'> 
    In order to get good marketing, it is paramount to understand the pool of guests 
    for any given company. If we are able to categorize guests into appropriate 
    groups, we can have targetted marketing for each segment.Getting any form of
    data from visitors in theme parks are very scarce. Therefore, an adjacent 
    industry will be analyzed. Customers in adjacent industry has to fulfil the 
    following characteristics that mimics the qualities of theme park revenues: 
    <b><em>presence of transactional sales; repetition of transactions</b></em>
    </p>
    """, unsafe_allow_html=True)

    mini_para_break()
    st.markdown(
    """<p style='font-size:20px; color:white;'> 
    </p>
    """, unsafe_allow_html=True)

    mini_para_break()

    st.markdown(
    """<p style='font-size:20px; color:white;'> 
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
    """<p style='font-size:20px; color:white;'> 
    We will be employing Recency Frequency Monetary framework (RFM) to characterize 
    all customers. 
    </p>
    """, unsafe_allow_html=True)
    mini_para_break()
    st.markdown("""
    <div style='font-size:20px; color:white;'>
    <div><b><em>Recency</b></em>: Number of days since last purchase</div>
    <div><b><em>Frequency</b></em>: Total number of unique transactions</div>
    <div><b><em>Monetary</b></em>: Total amount spent in purchases</div>
    </div>
    """, unsafe_allow_html=True)

    mini_para_break()
    st.markdown(
    """<p style='font-size:20px; color:white;'> 
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
    """<p style='font-size:20px; color:white;'> 
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
    st.plotly_chart(fig, key='Actual')

    st.markdown('<a name="tailoredmarketting"></a>', unsafe_allow_html=True)  # Anchor
    st.markdown(f"<h3 class='subheading'>Marketing Guest Segmentation: Tailored Marketing</h3>",
                unsafe_allow_html=True)
    st.markdown(f"<h5 class='subsubheading'>Champions</h5>",
                unsafe_allow_html=True)
    st.markdown(
    """<p style='font-size:20px; color:white;'> 
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
    """<p style='font-size:20px; color:white;'> 
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
    """<p style='font-size:20px; color:white;'> 
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
    """<p style='font-size:20px; color:white;'> 
    'Hibernating' customers come in last ranked across the RMF framework. They are
    inactive, making low-value purchase and not often. This could be a result of 
    discontent with company product. Therefore, the company could tap into 
    feedback-based marketing where the company obtain customer sentiment as well as
    pain points, and to reward for their time, they get exclusive discount coupons 
    for their next purchase. In addition, the company can include low-cut 
    touchpoints for these users, such as free subscription to company newsletters 
    showcasing new product listings. Lastly, to draw savings-based attention towards
    customers, the company can leverage on reactivation-based marketing, offering
    "We want you back" exclusive discounts to such customers.</p>
    """, unsafe_allow_html=True)
    
with tab3:
    st.markdown(
    f"""<h3 class='subheading'>
    Campaign Clustering: Key Findings
    </h1>
    """,unsafe_allow_html=True)

    st.markdown(
    """<p style='font-size:20px; color:white;'>
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
    """<p style='font-size:20px; color:white;'>
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
    """<p style='font-size:20px; color:white;'>
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
    """<p style='font-size:20px; color:white;'>
    Determinants of campaign effect now consists of... </p>
    """,
    unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:20px; color:white;'>
    <div><b><em>Absolute Marketing Lift</b></em>: absolute increase one month post campaigns, accounting for seasonality</div>
    <div><b><em>Percentage Marketing Lift</b></em>: percentage increase one month post campaigns, accounting for seasonality</div>
    <div><b><em>Average Crowd Level</b></em>: crowd level the month before the campaign</div>
    </div>
    """, unsafe_allow_html=True)

    mini_para_break()

    st.markdown(f"<h3 class='subheading'>Campaign Clustering: Findings</h1>",
                unsafe_allow_html=True)

    st.markdown("""<p style='font-size:20px; color:white;'>            
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

    st.markdown("""<p style='font-size:20px; color:white;'>         
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
    """<p style='font-size:20px; color:white;'> 
    From <a href="#mathref1">PC_1's equation</a>, can deduce that higer marketing 
    lifts (absolute/relative lifts) and lower monthly average crowd levels the month
    before campaigns are an indication of better marketing, vice versa. Companies
    can therefore use this algorithm to benchmark against their upcoming marketing
    efforts to conduct a review on how well their marketing strategies are.  
    </p>
    """, unsafe_allow_html=True)





references = ['https://www.statista.com/statistics/286526/coca-cola-advertising-spending-worldwide/',]
