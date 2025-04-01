import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

def KM_all(df):

    df_km = df.copy()
    df_km['Visit_Type_Code'] = df_km['Visit_Type'].astype('category').cat.codes
    df_km['Continent_Code'] = df_km['Continent'].astype('category').cat.codes

    features = ['Rating', 'Sentiment', 'Month', 'Visit_Type_Code', 'Continent_Code']
    X = df_km[features]

    # Determine inertia and silhouette scores for different numbers of clusters
    inertia = []
    sil_scores = []
    k_range = range(2, 10)

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42)
        labels = km.fit_predict(X)
        inertia.append(km.inertia_)
        score = silhouette_score(X, labels)
        sil_scores.append(score)

    # Plot the Elbow Method and Silhouette Scores
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(k_range, inertia, marker='o', color='blue')
    plt.title('Elbow Method for KMeans')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    
    plt.subplot(1, 2, 2)
    plt.plot(k_range, sil_scores, marker='o', color='green')
    plt.title('Silhouette Score for KMeans')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Score')
    
    plt.tight_layout()
    plt.show()

    # Optimal K based on the plots, in which k=5 was decided
    optimal_k = 5
    kmeans = KMeans(n_clusters=optimal_k, random_state=42)
    df_km['KMeans_Cluster'] = kmeans.fit_predict(X)

    # PCA transformation for visualization
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(X)

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=pca_components[:, 0], y=pca_components[:, 1], 
                    hue=df_km['KMeans_Cluster'], palette='Set3')
    plt.title(f'KMeans Clustering (k={optimal_k}) in PCA Space')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.legend(title="Cluster")
    plt.show()

    # Pairplot of features by KMeans Cluster
    sns.pairplot(df_km, vars=features, hue='KMeans_Cluster', palette='Set3')
    plt.suptitle('Pairplot of Features by KMeans Cluster', y=1.02)
    plt.show()

    # Compute and print cluster descriptive statistics
    cluster_profile = df_km.groupby('KMeans_Cluster')[['Rating', 'Sentiment', 'Month', 'Visit_Type_Code', 'Continent_Code']].describe()
    print("KMeans Cluster Descriptive Statistics:\n")
    print(cluster_profile)

if __name__ == "__main__":
    pass
