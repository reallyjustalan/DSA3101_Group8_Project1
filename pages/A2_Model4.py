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

import dataprocessing

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "../data/A2/updated_disneylandreviews.csv")
df = dataprocessing.load_and_clean_data(csv_path)

df_all = df
df_hongkong = df_all[df_all['Branch'] == 'Disneyland_HongKong']
df_california = df_all[df_all['Branch'] == 'Disneyland_California']
df_paris = df_all[df_all['Branch'] == 'Disneyland_Paris']

def main():
    st.title("KMeans Clustering Analysis by Continent")
    
    df = df_all
    
    df["Mismatch"] = df["Rating"] - (df["Sentiment"] * 5)
    df["Visit_Type_code"] = df["Visit_Type"].astype('category').cat.codes
    df["Branch_code"] = df["Branch"].astype('category').cat.codes
    
    features = ["Rating", "Sentiment", "Month", "Mismatch", "Visit_Type_code", "Branch_code"]
    continents = df["Continent"].unique()
    
    for cont in continents:
        df_subset = df[df["Continent"] == cont].copy()
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
        
        # PCA for dimensionality reduction
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
        axes[0].set_title(f"KMeans (PCA) - {cont}")
        axes[0].set_xlabel("PCA Component 1")
        axes[0].set_ylabel("PCA Component 2")
        
        # Right: Hierarchical dendrogram
        dendrogram(linked, truncate_mode='level', p=4, ax=axes[1])
        axes[1].set_title(f"Hierarchical Dendrogram - {cont}")
        axes[1].set_xlabel("Samples")
        axes[1].set_ylabel("Distance")
        
        plt.tight_layout()
        st.subheader(f"Clustering Results for {cont}")
        st.pyplot(fig)
      
      
      
if __name__ == "__main__":
    main()
     
           
st.markdown(
        """
        Based on the clustering analysis using features such as Rating, Sentiment, Month, and Mismatch (along with demographic proxies like Visit_Type and Branch), several key insights emerged:

North America: Clusters show high overall ratings, yet certain segments exhibit rating-sentiment mismatches, suggesting that while guests generally rate highly, underlying issues may be masked.

Asia: Distinct seasonal variations are evident, with some segments over-rating during peak periods despite moderate sentiment. This indicates cultural or seasonal factors influencing the experience.

Europe: Clusters are more balanced, with closer alignment between ratings and sentiment, reflecting consistently positive guest experiences.

Oceania: Though data volume is lower, guest profiles appear stable and balanced across clusters.

Africa & South America: These regions display heterogeneous clusters, suggesting varied guest experiences that warrant deeper local investigation.

Actionable Recommendations:

Conduct targeted follow-up surveys in regions with significant mismatches (e.g., North America and Asia) to uncover and address hidden pain points.

Leverage season-specific promotions and service enhancements in Asia and North America.

Sustain high-quality experiences in Europe and Oceania through loyalty initiatives.

Perform localized studies in Africa and South America to tailor interventions.
"""""
)

