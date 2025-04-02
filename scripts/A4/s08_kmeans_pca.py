from s06_analysis_avg_crowd import get_lift_of_campaign, df_crowd
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

lift1 = get_lift_of_campaign(df_crowd, 'Disney Magic Kingdom', '2023-03-01', 'Tron Light Cycle Run')
lift2 = get_lift_of_campaign(df_crowd, 'Epcot', '2023-10-01', 'Journey Of Water')
lift3 = get_lift_of_campaign(df_crowd, 'Tokyo DisneySea', '2023-12-01', 'Fantasy Spring')
lift4= get_lift_of_campaign(df_crowd, 'Universal Studios At Universal Orlando', '2023-12-01', 'Dreamworks Land')        
lift5 =get_lift_of_campaign(df_crowd, 'Six Flags Great America', '2024-08-01', 'Freight Fest')        
lift6= get_lift_of_campaign(df_crowd, 'Seaworld Orlando', '2023-05-01', 'Pipeline: The Surf Coaster')       
lift7= get_lift_of_campaign(df_crowd, 'Legoland California', '2024-03-01', 'Dino Valley')
lift8= get_lift_of_campaign(df_crowd, 'Disney California Adventure', '2017-04-01', 'Guardians Of The Galaxy',True)

theme_parks = ['Magic Kingdom', 'Epcot', 'Tokyo DisneySea', \
    'Universal Studios At Universal Orlando', 'Six Flags Great America',\
    'Seaworld Orlando', 'Legoland California', 'Disney California Adventure']
campaign = ['Tron Light Cycle Run', 'Jouney Of Water', 'Fantasy Spring', \
    'DreamWorks Land', 'Freight Fest', 'Pipeline: The Surf Coaster', \
    'Dino Valley', 'Guardians Of The Galaxy']
all_lifts = [lift1, lift2,lift3, lift4, lift5, lift6, lift7, lift8]
absolute_lifts = [lift[0] for lift in all_lifts]
relative_lifts = [lift[1] for lift in all_lifts]
avg_crowd_campaign_month = [lift[2] for lift in all_lifts]

campaign_df = pd.DataFrame({'theme_parks':theme_parks, 'campaign':campaign, \
    'avg_crowd_campaign_month':avg_crowd_campaign_month, \
    'absolute_lifts':absolute_lifts, 'relative_lifts': relative_lifts})

def get_dendrogram(campaign_df):    
    X = campaign_df.select_dtypes('float')
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    Z = linkage(X_scaled, method='ward')
    fig,ax = plt.subplots(figsize=(8,6))
    
    # plt.figure(figsize=(10,8))
    dendrogram(Z, labels = campaign_df['campaign'].values)

    return fig, ax
    # plt.title('Campaign Clusters')
    # plt.xticks(rotation=45)
    # plt.show()
    


# standardize numerical columns
def plot_clusters(campaign_df):
    X = campaign_df[['avg_crowd_campaign_month', 'absolute_lifts', 'relative_lifts']]
    X_scaled = StandardScaler().fit_transform(X)

    # fit and assign cluster labels to each campaign  
    kmeans_model = KMeans(n_clusters=2, random_state=731).fit(X_scaled)
    campaign_df['cluster'] = kmeans_model.labels_

    # visualise using PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    campaign_df['First PC'], campaign_df['Second PC'] = X_pca[:,0], X_pca[:, 1]

    plt.figure(figsize=(8,6))
    colors = ['mediumseagreen', 'red']

    # plot second component against first component with clusters
    for i, cluster in enumerate(campaign_df['cluster'].unique()):
        cluster_df = campaign_df[campaign_df['cluster'] == cluster]
        label='Bad'
        if cluster == 0:
            label='Good'
        plt.scatter(cluster_df['First PC'], cluster_df['Second PC'], \
            color=colors[i], label=f'{label} Campaign Cluster')
        for _, row in cluster_df.iterrows():
            plt.annotate(row['campaign'], \
                            (row['First PC'], row['Second PC']),
                            xytext=(5, 5), # make sure text is away from point
                            textcoords='offset pixels',
                            fontsize=7
                            ) 
        # Draw circle to visualise kmeans
        center = cluster_df[['First PC', 'Second PC']].mean().values
        radius = np.std(cluster_df[['First PC', 'Second PC']].values) * 1.5
        circle = plt.Circle(center, radius, color=colors[i], alpha=0.1)
        plt.gca().add_patch(circle)

        
            
    plt.legend()
    plt.title('Campaign Clusters (KMeans Clustering, PCA Visualisation)')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.show()
    
