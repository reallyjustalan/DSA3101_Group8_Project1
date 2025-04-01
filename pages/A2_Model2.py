import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import sys
import streamlit as st
from pathlib import Path
import os

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
    st.title("KMeans Analysis on all data")

    df_km = df_all.copy()
    df_km['Visit_Type_Code'] = df_km['Visit_Type'].astype('category').cat.codes
    df_km['Continent_Code'] = df_km['Continent'].astype('category').cat.codes

    features = ['Rating', 'Sentiment', 'Month', 'Visit_Type_Code', 'Continent_Code']
    X = df_km[features]

    # Compute inertia and silhouette scores for different numbers of clusters
    inertia = []
    sil_scores = []
    k_range = range(2, 10)
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42)
        labels = km.fit_predict(X)
        inertia.append(km.inertia_)
        score = silhouette_score(X, labels)
        sil_scores.append(score)

    # Plot Elbow Method and Silhouette Score
    fig1, ax1 = plt.subplots(1, 2, figsize=(12, 5))
    ax1[0].plot(list(k_range), inertia, marker='o', color='blue')
    ax1[0].set_title('Elbow Method for KMeans')
    ax1[0].set_xlabel('Number of Clusters')
    ax1[0].set_ylabel('Inertia')

    ax1[1].plot(list(k_range), sil_scores, marker='o', color='green')
    ax1[1].set_title('Silhouette Score for KMeans')
    ax1[1].set_xlabel('Number of Clusters')
    ax1[1].set_ylabel('Silhouette Score')
    fig1.tight_layout()

    st.subheader("Elbow Method and Silhouette Score")
    st.pyplot(fig1)

    # Assume optimal K based on the plots (here, we choose k=5)
    optimal_k = 5
    kmeans = KMeans(n_clusters=optimal_k, random_state=42)
    df_km['KMeans_Cluster'] = kmeans.fit_predict(X)

    # PCA for visualization of clusters
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(X)
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        x=pca_components[:, 0],
        y=pca_components[:, 1],
        hue=df_km['KMeans_Cluster'],
        palette='Set3',
        ax=ax2
    )
    ax2.set_title(f'KMeans Clustering (k={optimal_k}) in PCA Space')
    ax2.set_xlabel('PCA Component 1')
    ax2.set_ylabel('PCA Component 2')
    ax2.legend(title="Cluster")
    fig2.tight_layout()

    st.subheader("KMeans Clustering in PCA Space")
    st.pyplot(fig2)

    # Pairplot of features by KMeans Cluster
    st.subheader("Pairplot of Features by KMeans Cluster")
    pairplot_grid = sns.pairplot(df_km, vars=features, hue='KMeans_Cluster', palette='Set3')
    st.pyplot(pairplot_grid.fig)

    # Compute and display descriptive statistics for each cluster
    cluster_profile = df_km.groupby('KMeans_Cluster')[
        ['Rating', 'Sentiment', 'Month', 'Visit_Type_Code', 'Continent_Code']
    ].describe()
    st.subheader("KMeans Cluster Descriptive Statistics")
    st.write(cluster_profile)
    
    st.markdown(
    """
    Cluster 0
Rating: ~4.25 (High)
Sentiment: ~0.64 (Moderate)
Month: ~5.56 (Late Spring/Early Summer: April–July range)

Interpretation:
These guests are generally satisfied (mean rating >4.0).
Text feedback is moderately positive but not as enthusiastic as some other clusters.
They tend to visit in late spring to early summer (April–July).

Actionable Insights:
Early-Summer Campaigns: Offer promotions or special packages for May–June travelers to reinforce their positive experience.
Nudge Higher Ratings: Since sentiment is a bit lower than expected for a 4.25 rating, consider small service improvements or better communication to convert “good” experiences into “great” ones.
Preemptive Support: Provide details about peak-season amenities, local events, or weather tips to manage expectations and reduce potential dissatisfaction.

Cluster 1
Rating: ~4.24 (High)
Sentiment: ~0.73 (High)
Month: ~10.55 (Fall to Early Winter: September–December range)

Interpretation:
Similar overall rating to Cluster 0, but sentiment is higher, indicating more positive or enthusiastic text reviews.
Visits concentrate in the fall/holiday season.

Actionable Insights:
Holiday & Festive Promotions: Leverage their higher sentiment around end-of-year festivities—e.g., Christmas, New Year’s, or autumn events.
Encourage Advocacy: Their strong sentiment suggests they’re more likely to share positive feedback on social media or review sites. Offer referral bonuses or loyalty points for reviews.
Seasonal Upsells: Focus on holiday-themed experiences (e.g., special dinners, holiday shows) that match their likely travel window.


Cluster 2
Rating: ~4.22 (Moderately High)
Sentiment: ~0.69 (Moderate-High)
Month: ~2.41 (Winter/Early Spring: January–April range)

Interpretation:
The largest cluster (9,875 guests), with decent ratings and sentiment.
Primarily traveling in winter or early spring.
Slightly lower average rating than Clusters 0 and 1, but still above 4.0.

Actionable Insights:
Winter Specials: Offer packages tailored for the January–March period (e.g., Valentine’s getaways, spring break deals).
Boost Engagement: If they have moderate sentiment, consider sending personalized follow-up surveys or loyalty offers to maintain goodwill.
Volume Advantage: As the biggest group, even small improvements in their experience can significantly impact overall ratings and revenue.

Cluster 3
Rating: ~4.29 (Second-highest)
Sentiment: ~0.64 (Similar to Cluster 0)
Month: ~9.95 (Late Summer to Fall: August–December)

Interpretation:
Very close to Cluster 0 in sentiment, but a slightly higher rating (4.29 vs. 4.25).
They visit in late summer through fall, peaking around September/October.
Somewhat paradoxical that sentiment is not higher despite a good rating, suggesting they might rate well but not elaborate positively in text.

Actionable Insights:
Bridge the Rating–Sentiment Gap: Investigate why text sentiment is moderate even though star ratings are high. Possibly these guests are concise or reserved in written feedback.
Focus on Seasonal Events: Many destinations have major events in August–November (e.g., fall festivals). Promote relevant experiences to maintain strong satisfaction.
Targeted Surveys or Interviews: To understand what they like most (they do rate you highly) and how to convert that into more enthusiastic word-of-mouth.

Cluster 4
Rating: ~4.14 (Lowest among the five, but still above 4.0)
Sentiment: ~0.72 (Fairly high text positivity)
Month: ~6.57 (Spring to Summer: April–August)

Interpretation:
A curious mix: lowest average rating yet relatively high sentiment (comparable to Cluster 1’s 0.73).
Visits occur in the late spring/summer window.
Possibly these guests are warm in their feedback but with specific complaints that lower their final rating.

Actionable Insights:
Investigate Rating Discrepancies: If they speak positively (sentiment ~0.72) but still give 4.14 on average, identify specific service gaps. Maybe a critical amenity or logistical issue.
Summer Experience Enhancements: Offer improved check-in processes, better air-conditioning, or summer activity bundles to address potential friction points.
Encourage Detailed Feedback: Their textual sentiment is positive; prompting them to share more detailed reviews might reveal easy fixes that could raise their ratings to match their sentiment.

Overall

Seasonal Patterns
Cluster 2 (largest) is a winter–early spring crowd, while Clusters 0 and 4 favor spring–summer, and Clusters 1 and 3 lean toward fall–winter.
Align promotions, events, and staffing levels with each cluster’s travel window.

Rating vs. Sentiment
Most clusters have 4.1–4.3 average ratings, but sentiment scores vary from ~0.64 to ~0.73.
Cluster 1 has a higher sentiment (0.73) but the same rating as 0 (~4.24–4.25).
Cluster 4 shows the lowest rating (4.14) yet fairly high sentiment (0.72), suggesting a mismatch worth investigating.

Actionable Insights
Cluster 0 & 3: Similar moderate sentiment (~0.64) but decent ratings. They might be short, matter-of-fact reviewers who rate well but don’t gush in text.
Cluster 1: Strong sentiment and good ratings, especially during the fall–winter season—ideal for holiday or end-of-year marketing.
Cluster 2: Largest group, with a winter/early-spring focus. Even small improvements can yield big gains in overall ratings and revenue.
Cluster 4: Needs attention to close the gap between positive text feedback and lower star ratings, especially during peak summer months.
"""
)

if __name__ == "__main__":
    main()