import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

def KMVisit(df):

    df["Mismatch"] = df["Rating"] - (df["Sentiment"] * 5)
    df["Branch_code"] = df["Branch"].astype('category').cat.codes
    df["Continent_code"] = df["Continent"].astype('category').cat.codes

    features = ["Rating", "Sentiment", "Month", "Mismatch", "Continent_code", "Branch_code"]

    # Get unique visit types from the 'Visit_Type' column
    visit_types = df["Visit_Type"].unique()

    # Process each visit type separately
    for vt in visit_types:
        df_subset = df[df["Visit_Type"] == vt].copy()
        df_subset = df_subset.dropna(subset=features)
        if df_subset.empty:
            continue

        # Scale features
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

        # Create side-by-side plots: left for KMeans (PCA) and right for the dendrogram
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Left: PCA scatter plot colored by KMeans cluster labels
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
        plt.show()

if __name__ == "__main__":
    pass
