# This script here is to format the code such that it is streamlit compatible. Please refer to the other scripts for the model.

import streamlit as st
import seaborn as sns
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage


def create_plots(df_all, df_hongkong, df_california, df_paris):
    figures = [] 

    fig1, axs = plt.subplots(3, 2, figsize=(14, 15))
    datasets = {
        "All Data": df_all,
        "Hong Kong": df_hongkong,
        "California": df_california,
        "Paris": df_paris
    }

    for name, data in datasets.items():
        axs[0, 0].plot(data.groupby('Continent')['Rating'].mean(), marker='o', label=name)
    axs[0, 0].set_title('Average Rating by Continent')
    axs[0, 0].set_xlabel('Continent')
    axs[0, 0].set_ylabel('Average Rating')
    axs[0, 0].legend()

    for name, data in datasets.items():
        axs[0, 1].plot(data.groupby('Continent')['Sentiment'].mean(), marker='o', label=name)
    axs[0, 1].set_title('Average Sentiment by Continent')
    axs[0, 1].set_xlabel('Continent')
    axs[0, 1].set_ylabel('Average Sentiment')
    axs[0, 1].legend()

    for name, data in datasets.items():
        axs[1, 0].plot(data.groupby('Month')['Rating'].mean(), marker='o', label=name)
    axs[1, 0].set_title('Average Rating by Month')
    axs[1, 0].set_xlabel('Month')
    axs[1, 0].set_ylabel('Average Rating')
    axs[1, 0].legend()

    for name, data in datasets.items():
        axs[1, 1].plot(data.groupby('Month')['Sentiment'].mean(), marker='o', label=name)
    axs[1, 1].set_title('Average Sentiment by Month')
    axs[1, 1].set_xlabel('Month')
    axs[1, 1].set_ylabel('Average Sentiment')
    axs[1, 1].legend()

    for name, data in datasets.items():
        axs[2, 0].plot(data.groupby('Year')['Rating'].mean(), marker='o', label=name)
    axs[2, 0].set_title('Average Rating by Year')
    axs[2, 0].set_xlabel('Year')
    axs[2, 0].set_ylabel('Average Rating')
    axs[2, 0].legend()

    for name, data in datasets.items():
        axs[2, 1].plot(data.groupby('Year')['Sentiment'].mean(), marker='o', label=name)
    axs[2, 1].set_title('Average Sentiment by Year')
    axs[2, 1].set_xlabel('Year')
    axs[2, 1].set_ylabel('Average Sentiment')
    axs[2, 1].legend()

    plt.tight_layout()
    figures.append(fig1) 

    fig2, axs2 = plt.subplots(1, 2, figsize=(14, 6))
    sns.countplot(x='Visit_Type', hue='Continent', data=df_all, ax=axs2[0], palette="Set3")
    axs2[0].set_title('Visit_Type Count by Continent')
    axs2[0].set_xlabel('Visit Type')
    axs2[0].set_ylabel('Count')

    sns.countplot(x='Visit_Type', hue='Branch', data=df_all, ax=axs2[1], palette="Set3")
    axs2[1].set_title('Visit_Type Count by Branch')
    axs2[1].set_xlabel('Visit Type')
    axs2[1].set_ylabel('Count')

    plt.tight_layout()
    figures.append(fig2)  

    fig3, axs3 = plt.subplots(2, 2, figsize=(14, 12))
    visit_rating = df_all.groupby('Visit_Type')['Rating'].mean()
    axs3[0, 0].bar(visit_rating.index, visit_rating.values, color='skyblue')
    axs3[0, 0].set_title('Average Rating for Visit_Type')
    axs3[0, 0].set_xlabel('Visit Type')
    axs3[0, 0].set_ylabel('Average Rating')

    visit_sentiment = df_all.groupby('Visit_Type')['Sentiment'].mean()
    axs3[0, 1].bar(visit_sentiment.index, visit_sentiment.values, color='salmon')
    axs3[0, 1].set_title('Average Sentiment for Visit_Type')
    axs3[0, 1].set_xlabel('Visit Type')
    axs3[0, 1].set_ylabel('Average Sentiment')

    sns.countplot(x='Branch', hue='Continent', data=df_all, ax=axs3[1, 0], palette="Set3")
    axs3[1, 0].set_title('Continent Count by Branch')
    axs3[1, 0].set_xlabel('Branch')
    axs3[1, 0].set_ylabel('Count')

    plt.tight_layout()
    figures.append(fig3) 

    return figures


def DBSCANmodel(df):
    df_dbscan = df.copy()

    df_dbscan['Visit_Type'] = df_dbscan['Visit_Type'].astype('category').cat.codes
    df_dbscan['Continent'] = df_dbscan['Continent'].astype('category').cat.codes

    features = ['Rating', 'Sentiment', 'Month', 'Visit_Type', 'Continent']

    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=1, min_samples=100)
    df_dbscan['DBSCAN_Cluster'] = dbscan.fit_predict(df_dbscan[features])

    fig1, axs = plt.subplots(1, 2, figsize=(12, 6))
    sns.boxplot(x='DBSCAN_Cluster', y='Rating', data=df_dbscan, palette="Set3", ax=axs[0])
    axs[0].set_title('DBSCAN Cluster Distribution for Rating')
    sns.boxplot(x='DBSCAN_Cluster', y='Sentiment', data=df_dbscan, palette="Set3", ax=axs[1])
    axs[1].set_title('DBSCAN Cluster Distribution for Sentiment')
    plt.tight_layout()

    dbscan_stats = df_dbscan.groupby('DBSCAN_Cluster')[['Rating', 'Sentiment', 'Month']].describe()

    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(df_dbscan[features])
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x=pca_components[:, 0], y=pca_components[:, 1],
                    hue=df_dbscan['DBSCAN_Cluster'], palette='Set3', ax=ax2)
    ax2.set_title('DBSCAN Clustering in PCA Space')

    return [fig1, fig2], dbscan_stats


def KM_all(df):

    df_km = df.copy()
    df_km['Visit_Type_Code'] = df_km['Visit_Type'].astype('category').cat.codes
    df_km['Continent_Code'] = df_km['Continent'].astype('category').cat.codes

    features = ['Rating', 'Sentiment', 'Month', 'Visit_Type_Code', 'Continent_Code']
    X = df_km[features]

    inertia = []
    sil_scores = []
    k_range = range(2, 10)
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42)
        labels = km.fit_predict(X)
        inertia.append(km.inertia_)
        score = silhouette_score(X, labels)
        sil_scores.append(score)

    # Elbow Method and Silhouette Score 
    fig1, axes1 = plt.subplots(1, 2, figsize=(12, 5))
    axes1[0].plot(list(k_range), inertia, marker='o', color='blue')
    axes1[0].set_title('Elbow Method for KMeans')
    axes1[0].set_xlabel('Number of Clusters')
    axes1[0].set_ylabel('Inertia')

    axes1[1].plot(list(k_range), sil_scores, marker='o', color='green')
    axes1[1].set_title('Silhouette Score for KMeans')
    axes1[1].set_xlabel('Number of Clusters')
    axes1[1].set_ylabel('Silhouette Score')
    fig1.tight_layout()

    optimal_k = 5
    kmeans = KMeans(n_clusters=optimal_k, random_state=42)
    df_km['KMeans_Cluster'] = kmeans.fit_predict(X)

    # PCA Scatter Plot of Clusters ---
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(X)
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x=pca_components[:, 0], y=pca_components[:, 1], 
                    hue=df_km['KMeans_Cluster'], palette='Set3', ax=ax2)
    ax2.set_title(f'KMeans Clustering (k={optimal_k}) in PCA Space')
    ax2.set_xlabel('PCA Component 1')
    ax2.set_ylabel('PCA Component 2')
    ax2.legend(title="Cluster")
    fig2.tight_layout()

    # Pairplot of Features by KMeans Cluster ---
    pairgrid = sns.pairplot(df_km, vars=features, hue='KMeans_Cluster', palette='Set3')
    fig3 = pairgrid.fig
    fig3.suptitle('Pairplot of Features by KMeans Cluster', y=1.02)
    fig3.tight_layout()


    cluster_profile = df_km.groupby('KMeans_Cluster')[features].describe()

    figures = [fig1, fig2, fig3]
    return figures, cluster_profile

def mm(df):

    df["mismatch"] = df["Rating"] - (df["Sentiment"] * 5)
    mismatch_stats = df["mismatch"].describe()
    
    # Create quantile-based mismatch segments
    df["mismatch_segment"] = pd.qcut(
        df["mismatch"],
        q=4,
        labels=["Low Mismatch", "Moderate Mismatch", "High Mismatch", "Very High Mismatch"]
    )
    segment_counts = df["mismatch_segment"].value_counts()
    
    X = df[["mismatch"]].values
    kmeans = KMeans(n_clusters=4, random_state=42)
    df["mismatch_cluster"] = kmeans.fit_predict(X)
    
    cluster_stats = df.groupby("mismatch_cluster")["mismatch"].agg(["mean", "count"])

    # Histogram of Mismatch

    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.hist(df["mismatch"], bins=50, alpha=0.7, color="skyblue", edgecolor="black")
    ax1.set_xlabel("Mismatch (Rating - Sentiment*5)")
    ax1.set_ylabel("Count")
    ax1.set_title("Distribution of Mismatch between Rating and Sentiment")
    plt.tight_layout()
    

    # KDE Plot by KMeans Cluster

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
    plt.tight_layout()
    

    # Boxplot of Mismatch by KMeans Cluster

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
    plt.tight_layout()
    
    figures = [fig1, fig2, fig3]
    return mismatch_stats, segment_counts, cluster_stats, figures

def KMContinent(df):

    df["Mismatch"] = df["Rating"] - (df["Sentiment"] * 5)
    df["Visit_Type_code"] = df["Visit_Type"].astype('category').cat.codes
    df["Branch_code"] = df["Branch"].astype('category').cat.codes

    features = ["Rating", "Sentiment", "Month", "Mismatch", "Visit_Type_code", "Branch_code"]

    continents = df["Continent"].unique()

    figures = []

    # Process each continent separately
    for cont in continents:
        df_subset = df[df["Continent"] == cont].copy()
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
        figures.append((cont, fig))
        
    return figures

def KMVisit(df):
    df["Mismatch"] = df["Rating"] - (df["Sentiment"] * 5)
    df["Branch_code"] = df["Branch"].astype('category').cat.codes
    df["Continent_code"] = df["Continent"].astype('category').cat.codes

    features = ["Rating", "Sentiment", "Month", "Mismatch", "Continent_code", "Branch_code"]

    visit_types = df["Visit_Type"].unique()
    figures = []

    for vt in visit_types:
        df_subset = df[df["Visit_Type"] == vt].copy()
        df_subset = df_subset.dropna(subset=features)
        if df_subset.empty:
            continue

        X = df_subset[features].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        kmeans = KMeans(n_clusters=4, random_state=42)
        kmeans_labels = kmeans.fit_predict(X_scaled)

        linked = linkage(X_scaled, method='ward')

        pca = PCA(n_components=2, random_state=42)
        X_pca = pca.fit_transform(X_scaled)

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
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
        
        dendrogram(linked, truncate_mode='level', p=4, ax=axes[1])
        axes[1].set_title(f"Hierarchical Dendrogram - {vt}")
        axes[1].set_xlabel("Samples")
        axes[1].set_ylabel("Distance")
        
        plt.tight_layout()
        figures.append((vt, fig))
        
    return figures