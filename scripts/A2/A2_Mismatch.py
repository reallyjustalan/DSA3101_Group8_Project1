import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def mm(df):
    
    # Compute mismatch between Rating and Sentiment
    df["mismatch"] = df["Rating"] - (df["Sentiment"] * 5)
    
    print("Mismatch Statistics:")
    print(df["mismatch"].describe())
    
    # Create quantile-based mismatch segments
    df["mismatch_segment"] = pd.qcut(
        df["mismatch"],
        q=4,
        labels=[
            "Low Mismatch", "Moderate Mismatch", "High Mismatch", "Very High Mismatch"
        ]
    )
    
    print("\nSegment Counts (Quantile-based):")
    print(df["mismatch_segment"].value_counts())
    
    # Perform KMeans clustering on the mismatch column
    X = df[["mismatch"]].values
    kmeans = KMeans(n_clusters=4, random_state=42)
    df["mismatch_cluster"] = kmeans.fit_predict(X)
    
    print("\nKMeans Mismatch Clusters (mean and count):")
    print(df.groupby("mismatch_cluster")["mismatch"].agg(["mean", "count"]))
    
    # Plot 1: Histogram of Mismatch
    plt.figure(figsize=(8, 6))
    plt.hist(df["mismatch"], bins=50, alpha=0.7, color="skyblue", edgecolor="black")
    plt.xlabel("Mismatch (Rating - Sentiment*5)")
    plt.ylabel("Count")
    plt.title("Distribution of Mismatch between Rating and Sentiment")
    plt.show()
    
    # Plot 2: KDE Plot by KMeans Cluster
    plt.figure(figsize=(8, 6))
    sns.kdeplot(
        data=df,
        x="mismatch",
        hue="mismatch_cluster", 
        fill=True,
        common_norm=False,      
        alpha=0.5
    )
    plt.title("Mismatch Distribution by KMeans Cluster")
    plt.xlabel("Mismatch (Rating - 5 * Sentiment)")
    plt.ylabel("Density")
    plt.show()
    
    # Plot 3: Boxplot of Mismatch by KMeans Cluster
    plt.figure(figsize=(8, 6))
    sns.boxplot(
        x="mismatch_cluster",  
        y="mismatch",
        data=df,
        palette="Set2"
    )
    plt.title("Mismatch Boxplot by KMeans Cluster")
    plt.xlabel("KMeans Cluster")
    plt.ylabel("Mismatch (Rating - 5 * Sentiment)")
    plt.show()

if __name__ == "__main__":
    pass
