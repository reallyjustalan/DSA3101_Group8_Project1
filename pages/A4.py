import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# change relative file path to import python files
sys.path.append('../scripts/A4')

import s08_kmeans_pca as s08
    
# st.set_page_config(
#     page_title='Marketing in Theme Parks',
#     page_icon = '📊',
#     layout ='wide',
#     initial_sidebar_state='expanded'
# )

st.markdown(f"<h1 class='header'>Marketing in Theme Parks </h1>", unsafe_allow_html=True)
st.badge('success!', icon=':material/done_all:', color='blue')

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


#INSERT FOOT NOTE
st.markdown(
"""<p style='font-size:24px; color:white;'>
To an average Joe, marketing may seem like the simple task of posting a campaign alert on Facebook, or handing out 
fliers promoting 20% discount at your nearby KBBQ restaurant. Unfortunately, this is not that simple. marketing is so 
much more involved than advertising. In fact, we see big players in the drink industry such as Coca Cola pouring over
$4.0 billion US dollars consistently for the past decade (with the exception of 2020 COVID-19 of course).</p>""", 
unsafe_allow_html=True)
big_para_break()

st.markdown(
"""
<p style='font-size:24px; color:white;'> In today's hyper-competitive marketplace, marketing is the cornerstone of 
business success—a disciplined strategy that transforms products into brands, customers into advocates, and markets 
into revenue streams. Marketing doesn't need to be complicated to be effective. At its core, it's about connecting the 
right product with the right customer—clearly, efficiently, and profitably. Whether you're a small business or a growing
brand, simple marketing focuses on three key principles...</p>
""",
unsafe_allow_html=True)

mini_para_break()

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

st.html('')
# unsafe_allow_html=True)

fig, ax = s08.get_dendrogram(s08.campaign_df)
ax.tick_params(axis='x', labelsize=8, rotation = 30)

st.pyplot(fig)



references = ['https://www.statista.com/statistics/286526/coca-cola-advertising-spending-worldwide/',
              ]
