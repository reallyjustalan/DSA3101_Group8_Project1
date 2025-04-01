import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA

def DBSCANmodel(df):

    df_dbscan = df.copy()

    # Convert categorical columns to numeric codes
    df_dbscan['Visit_Type'] = df_dbscan['Visit_Type'].astype('category').cat.codes
    df_dbscan['Continent'] = df_dbscan['Continent'].astype('category').cat.codes

    # Define the features to be used in DBSCAN clustering
    features = ['Rating', 'Sentiment', 'Month', 'Visit_Type', 'Continent']

    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=1, min_samples=100)  
    df_dbscan['DBSCAN_Cluster'] = dbscan.fit_predict(df_dbscan[features])

    # Figure 1: Boxplots for DBSCAN Clusters 
    plt.figure(figsize=(12, 6))

    # Boxplot: Cluster Distribution for Rating
    plt.subplot(1, 2, 1)
    sns.boxplot(x='DBSCAN_Cluster', y='Rating', data=df_dbscan, palette="Set3")
    plt.title('DBSCAN Cluster Distribution for Rating')

    # Boxplot: Cluster Distribution for Sentiment
    plt.subplot(1, 2, 2)
    sns.boxplot(x='DBSCAN_Cluster', y='Sentiment', data=df_dbscan, palette="Set3")
    plt.title('DBSCAN Cluster Distribution for Sentiment')

    plt.tight_layout()
    plt.show()

    # Compute and Display DBSCAN Descriptive Statistics
    dbscan_stats = df_dbscan.groupby('DBSCAN_Cluster')[['Rating', 'Sentiment', 'Month']].describe()
    print("DBSCAN Cluster Descriptive Statistics:\n")
    print(dbscan_stats)

    # Figure 2: Visualizing DBSCAN Clusters in PCA Space 
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(df_dbscan[features])

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=pca_components[:, 0], y=pca_components[:, 1],
                    hue=df_dbscan['DBSCAN_Cluster'], palette='Set3')
    plt.title('DBSCAN Clustering in PCA Space')
    plt.show()

if __name__ == "__main__":
    pass
