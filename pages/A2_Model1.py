import sys
import streamlit as st
from pathlib import Path
import os
import seaborn as sns
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

BASE_DIR = Path(__file__).resolve().parent.parent 
scripts_a2_path = BASE_DIR / "scripts" / "A2"
sys.path.append(str(scripts_a2_path))

import A2_dataprocessing

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "../data/A2/updated_disneylandreviews.csv")
df = A2_dataprocessing.load_and_clean_data(csv_path)

df_all = df
df_hongkong = df_all[df_all['Branch'] == 'Disneyland_HongKong']
df_california = df_all[df_all['Branch'] == 'Disneyland_California']
df_paris = df_all[df_all['Branch'] == 'Disneyland_Paris']


def main():
    st.title("DBSCAN analysis on all data")
    df_all = df

    df_dbscan = df_all.copy()
    df_dbscan['Visit_Type'] = df_dbscan['Visit_Type'].astype('category').cat.codes
    df_dbscan['Continent'] = df_dbscan['Continent'].astype('category').cat.codes
    features = ['Rating', 'Sentiment', 'Month', 'Visit_Type', 'Continent']
    dbscan = DBSCAN(eps=1, min_samples=100)
    df_dbscan['DBSCAN_Cluster'] = dbscan.fit_predict(df_dbscan[features])
    
    # Figure 1: Boxplots for DBSCAN Clusters ---
    fig1, ax = plt.subplots(1, 2, figsize=(12, 6))
    sns.boxplot(x='DBSCAN_Cluster', y='Rating', data=df_dbscan, palette="Set3", ax=ax[0])
    ax[0].set_title('DBSCAN Cluster Distribution for Rating')
    sns.boxplot(x='DBSCAN_Cluster', y='Sentiment', data=df_dbscan, palette="Set3", ax=ax[1])
    ax[1].set_title('DBSCAN Cluster Distribution for Sentiment')
    fig1.tight_layout()
    st.pyplot(fig1)  

    # Compute and Display DBSCAN Descriptive Statistics ---
    dbscan_stats = df_dbscan.groupby('DBSCAN_Cluster')[['Rating', 'Sentiment', 'Month']].describe()
    st.subheader("DBSCAN Cluster Descriptive Statistics")
    st.write(dbscan_stats)

    # Figure 2: Visualizing DBSCAN Clusters in PCA Space ---
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(df_dbscan[features])
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x=pca_components[:, 0], y=pca_components[:, 1],
                    hue=df_dbscan['DBSCAN_Cluster'], palette='Set3', ax=ax2)
    ax2.set_title('DBSCAN Clustering in PCA Space')
    fig2.tight_layout()
    st.pyplot(fig2)
    
    st.markdown(
    """
    Cluster -1 (Noise/Outliers)

These points do not fit into any cluster's density, but these reviews aren't necessarily good or bad, but rather unusual combinations of the features that did not meet any of the other density threshold. This group might contain visitors from less common months or continent, or with a combination of moderate rating and sentiment that places them outside the denser regions of the data. 

Cluster 0 (Moderate Satisfaction)

Demographics (Hypothetical)
Families, couples, or regular travelers who look for a reliable, comfortable experience.
Likely a diverse age range, but share a preference for consistent quality.

Behavioral Attributes
Rating: High average (4.71), fairly close to 5.
Sentiment: Positive (0.73), indicating mostly favorable comments.
Timing: Average month ~6.93, suggesting they favor summer visits (June/July).

Preference-Based Insights
Appreciate a well-rounded, reliable experience (good service, clean facilities).
May be open to slight up-sells if they see clear value.
Not as vocal or enthusiastic as Cluster 1, but still content and likely to return.

Actionable Insights
Maintain Quality: Focus on consistency in service, room quality, and dining experiences.
Upselling Opportunities: Offer add-ons (e.g., tours, spa packages) that enhance the experience without risking dissatisfaction.
Retention Programs: Introduce loyalty or membership perks to convert them into repeat customers.

Cluster 1 (High Satisfaction)

Demographics (Hypothetical)
Possibly more experienced travelers or those loyal to the brand.
Could be mid- to higher-income individuals who value excellent service and are willing to pay for it.

Behavioral Attributes
Rating: 4.70—nearly identical to Cluster 0, but with a slightly broader distribution.
Sentiment: 0.84, the highest among all clusters, indicating very positive written feedback.
Timing: Average month ~6.84 (also around June/July), similar to Cluster 0.

Preference-Based Insights
Value the intangible aspects of a stay (personalized service, brand recognition, loyalty benefits).
More likely to leave detailed, positive reviews or recommend to friends/family.

Actionable Insights
Referral & Ambassador Programs: Encourage them to share their positive experiences on social media or review platforms.
Personalization: Recognize repeat visits with personalized welcomes or exclusive perks.
Community Building: Invite them to loyalty clubs or events where they can connect with other loyal customers.

Cluster 2 (Extremely Satisfied)

Demographics (Hypothetical)
Could be VIPs, premium travelers, or a specialized segment (e.g., event attendees, honeymooners).
Possibly smaller groups or individuals traveling for a unique occasion.

Behavioral Attributes
Count: Only 92, making this the smallest cluster.
Rating: 4.99, nearly perfect. Standard deviation is extremely low (~0.10).
Sentiment: 0.80, also quite high (close to Cluster 1).
Timing: Average month ~1.01, indicating January visits—possibly tied to holiday or New Year’s events.

Preference-Based Insights
They consistently have an outstanding experience (almost always 5-star reviews).
Likely highly motivated by special occasions, unique offerings, or seasonal events.

Actionable Insights
Exclusive Experiences: Provide VIP treatment, early access, or premium event invitations.
Leverage Seasonality: If these are holiday guests, create special New Year’s packages or promotions to keep them returning.
High-Touch Service: Personalized communication, follow-up thank-you notes, or direct phone calls to build loyalty.

Overall Takeaways
Retain & Delight Cluster 0
Keep service consistent, offer moderate upsells, encourage loyalty sign-ups.

Empower Cluster 1
Tap into their enthusiasm with referral programs, personalized perks, and brand advocacy.

Celebrate Cluster 2
Provide ultra-personalized experiences, highlight seasonal or exclusive events, and maintain top-notch service for this niche group.
"""
)
    

if __name__ == "__main__":
    main()

