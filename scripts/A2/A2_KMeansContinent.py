import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

def KMContinent(df):
    df["Mismatch"] = df["Rating"] - (df["Sentiment"] * 5)
    df["Visit_Type_code"] = df["Visit_Type"].astype('category').cat.codes
    df["Branch_code"] = df["Branch"].astype('category').cat.codes

    features = ["Rating", "Sentiment", "Month", "Mismatch", "Visit_Type_code", "Branch_code"]

    # Get the unique continents
    continents = df["Continent"].unique()

    # Process each continent separately
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

        # PCA for dimensionality reduction for visualization
        pca = PCA(n_components=2, random_state=42)
        X_pca = pca.fit_transform(X_scaled)

        # Plot side by side: Left for KMeans clustering (PCA scatter) and right for the dendrogram
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Left: PCA scatter plot colored by KMeans cluster
        scatter = axes[0].scatter(
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
        plt.show()

if __name__ == "__main__":
    pass
