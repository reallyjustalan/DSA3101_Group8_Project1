import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
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
    st.title("Mismatch Analysis")

    df = df_all

    df["mismatch"] = df["Rating"] - (df["Sentiment"] * 5)

    st.write("### Mismatch Statistics")
    st.write(df["mismatch"].describe())

    # Create quantile-based mismatch segments
    df["mismatch_segment"] = pd.qcut(
        df["mismatch"],
        q=4,
        labels=["Low Mismatch", "Moderate Mismatch", "High Mismatch", "Very High Mismatch"]
    )
    
    st.write("### Mismatch Segment Counts (Quantile-based)")
    st.write(df["mismatch_segment"].value_counts())

    # KMeans Clustering on Mismatch
    X = df[["mismatch"]].values
    kmeans = KMeans(n_clusters=4, random_state=42)
    df["mismatch_cluster"] = kmeans.fit_predict(X)

    st.write("### KMeans Mismatch Clusters (Mean & Count)")
    cluster_stats = df.groupby("mismatch_cluster")["mismatch"].agg(["mean", "count"])
    st.write(cluster_stats)

    # Plot 1: Histogram of Mismatch
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.hist(df["mismatch"], bins=50, alpha=0.7, color="skyblue", edgecolor="black")
    ax1.set_xlabel("Mismatch (Rating - Sentiment*5)")
    ax1.set_ylabel("Count")
    ax1.set_title("Distribution of Mismatch between Rating and Sentiment")
    st.pyplot(fig1)

    # Plot 2: KDE Plot by KMeans Cluster
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.kdeplot(
        data=df,
        x="mismatch",
        hue="mismatch_cluster",
        fill=True,
        common_norm=False,
        alpha=0.5,
        ax=ax2
    )
    ax2.set_title("Mismatch Distribution by KMeans Cluster")
    ax2.set_xlabel("Mismatch (Rating - 5 * Sentiment)")
    ax2.set_ylabel("Density")
    st.pyplot(fig2)

    # Plot 3: Boxplot of Mismatch by KMeans Cluster
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    sns.boxplot(
        x="mismatch_cluster",
        y="mismatch",
        data=df,
        palette="Set2",
        ax=ax3
    )
    ax3.set_title("Mismatch Boxplot by KMeans Cluster")
    ax3.set_xlabel("KMeans Cluster")
    ax3.set_ylabel("Mismatch (Rating - 5 * Sentiment)")
    st.pyplot(fig3)
    
    st.markdown(
    """
    Cluster 0: Extreme Over-Raters

Mean mismatch ~6.23, which is quite high.
These guests often give 4–5 star ratings even though their sentiment is more moderate or low.
Possible Reasons: They might be polite or feel obligated to leave a high rating, or they may quickly click 5 stars but express concerns in the text.
Business Takeaway: Look at their negative or lukewarm comments despite the high rating to identify hidden issues or unmet expectations.

Cluster 1: Mostly Aligned
Largest group (~22k guests), with a mean mismatch ~0.38.
Their star ratings and sentiment are fairly consistent—slightly over the text sentiment, but not by much.
Possible Reasons: They likely rate and comment with similar feelings. Minor rounding-up of the star rating could happen (e.g., 4.5 in mind, but they click 5).
Business Takeaway: This group is straightforward; what they say in text largely matches how they rate. Focus on maintaining their positive experience.

Cluster 2: Under-Raters
Mean mismatch ~–1.22 (negative).
These guests express fairly positive sentiment in text but give a lower star rating.
Possible Reasons: Perhaps a single negative aspect overshadowed an otherwise good experience, or they are harsher in numeric ratings.
Business Takeaway: They sound satisfied in reviews, but the numeric rating doesn’t reflect that. Investigate consistent pain points (e.g., price vs. value) that prompt them to rate lower than their words suggest.

Cluster 3: Moderate Over-Raters
Mean mismatch ~2.60, which is over-rating but not as extreme as Cluster 0.
They’re giving star ratings that exceed the tone of their text feedback, but less dramatically than Cluster 0.
Possible Reasons: They may be mostly happy but mention smaller issues in text. They still give a 4 or 5 star rating overall.
Business Takeaway: Compare their textual feedback to their final ratings to see what improvements could turn them into fully satisfied, consistently positive reviewers.

Possible Next Steps

Targeted Follow-Up for Extreme Over-Raters (Cluster 0)
Don’t be misled by the high star rating. Their text indicates they’re not as happy as the rating suggests.
Consider sending surveys or personal follow-ups to pinpoint their concerns.

Maintain Satisfaction for Mostly Aligned Guests (Cluster 1)
These are the “straight shooters.” Their feedback is a reliable indicator of their overall satisfaction.
Keep doing what’s working, and address any small suggestions for improvement.

Win Over the Under-Raters (Cluster 2)
These guests are the opposite of Cluster 0: they like your service (positive text), but the final rating is still under 5.
Quick wins might involve addressing minor annoyances, better price-value alignment, or clarifying amenities.

Nudge Moderate Over-Raters (Cluster 3)
They generally give good ratings but mention specific issues.
Fixing those recurring issues can turn them into truly happy advocates whose text sentiment matches (or exceeds) their numeric rating.
"""
)

if __name__ == "__main__":
    main()
