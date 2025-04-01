import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
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
    st.title("Clustering Analysis by Visit Type")

    df = df_all
    
    df["Mismatch"] = df["Rating"] - (df["Sentiment"] * 5)
    df["Branch_code"] = df["Branch"].astype('category').cat.codes
    df["Continent_code"] = df["Continent"].astype('category').cat.codes

    features = ["Rating", "Sentiment", "Month", "Mismatch", "Continent_code", "Branch_code"]

    visit_types = df["Visit_Type"].unique()

    for vt in visit_types:
        df_subset = df[df["Visit_Type"] == vt].copy()
        df_subset = df_subset.dropna(subset=features)
        if df_subset.empty:
            continue

        X = df_subset[features].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # KMeans Clustering
        kmeans = KMeans(n_clusters=4, random_state=42)
        kmeans_labels = kmeans.fit_predict(X_scaled)

        # Hierarchical Clustering
        linked = linkage(X_scaled, method='ward')

        # PCA for visualization
        pca = PCA(n_components=2, random_state=42)
        X_pca = pca.fit_transform(X_scaled)

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Left: PCA scatter plot colored by KMeans cluster
        axes[0].scatter(
            X_pca[:, 0],
            X_pca[:, 1],
            c=kmeans_labels,
            cmap="Set2",
            alpha=0.7
        )
        axes[0].set_title(f"KMeans (PCA) - {vt}")
        axes[0].set_xlabel("PCA Component 1")
        axes[0].set_ylabel("PCA Component 2")

        # Right: Hierarchical dendrogram
        dendrogram(linked, truncate_mode='level', p=4, ax=axes[1])
        axes[1].set_title(f"Hierarchical Dendrogram - {vt}")
        axes[1].set_xlabel("Samples")
        axes[1].set_ylabel("Distance")

        plt.tight_layout()
        st.subheader(f"Clustering Analysis for Visit Type: {vt}")
        st.pyplot(fig)
        
if __name__ == "__main__":
    main()   
        
st.markdown(
        """
        Key Insights

Unknown: Large, diverse group with broad distributions in both PCA and dendrogram, suggesting mixed traveler profiles. Clusters may reflect varying regional or branch preferences, implying a need for more targeted data collection to better understand motivations.

Family: Dense clustering indicates consistent patterns—likely higher ratings and sentiment, plus moderate mismatch. Families appear more homogeneous, focusing on reliable, kid-friendly experiences.

Friends: Wider spread in PCA space suggests diverse priorities. Some clusters show strong ratings but moderate sentiment, hinting at hidden dissatisfaction or unmet group expectations (e.g., queue times, group deals).

Couples: Fewer data points yield tighter clusters, suggesting specialized needs (romantic experiences, privacy, or upgraded amenities). Ratings may be high, but mismatch spikes if expectations aren’t met.

Solo: Smallest dataset with scattered clusters. Likely niche travelers who might value flexibility, solitude, or unique offerings. Even minor improvements (e.g., single-rider lines, solo-friendly dining) could boost loyalty.

Actionable Recommendations

Unknown: Encourage more specific visit-type identification (e.g., surveys, booking forms) to tailor marketing and understand preferences.

Family: Maintain kid-friendly features and consistent service; highlight new family-focused attractions to enhance loyalty.

Friends: Offer group discounts, flexible packages, and social experiences (e.g., photo spots, meet-and-greets) to address hidden pain points.

Couples: Develop romantic packages, premium add-ons, or exclusive dining to meet higher expectations.

Solo: Provide single-rider lines, personal itineraries, and unique experiences to differentiate the park for independent travelers.

Overall Comment

Each visit type displays distinct clustering patterns across features (Rating, Sentiment, Month, Mismatch, Continent, Branch). Families show consistency, while couples and solo travelers are smaller but have more specialized demands. Friends exhibit a broad range of preferences, and the large “Unknown” group suggests an opportunity for better segmentation and targeted offerings.
        """
        )

