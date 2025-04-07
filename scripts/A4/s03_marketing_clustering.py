#####################################
# author: Chris Yong Hong Sen
# date: 02 Apr 2025
# preamble: Cluster 7 campaigns to good and bad
# 
# pre-req: machine learning data preprocessing, unsupervised learning KMeans 
#          algorithm, distance based ML algorithms (dendograms)
#
# additional notes: campaign_df, get_dendrogram() and get_clusters() are used
#                   in final webpage ../../pages/A4.py
#           
######################################
from scripts.A4.s02_analysis_avg_crowd import get_lift_of_campaign, df_crowd
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def get_dendrogram(campaign_df):    
    """returns fig, ax objects in preparation for streamlit rendering

    Args:
        campaign_df (pandas.DataFrame): a monthly time series of monthly crowd
                                        level for campaigns 

    Returns:
        tuple(matplotlib.figure, matplotlib.axes.Axes): a fig object and ax 
                                                        object
                                                        
    Additional Notes:
        This function is strictly used by the developer to visualize KMeans
        decision algorithm by seeing the decision points via similar distance 
        based algorithms
    """
    # select features
    X = campaign_df.select_dtypes('float')
    
    # scale features to ensure equal representation of each feature
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # fit the dendrogram to scaled features
    Z = linkage(X_scaled, method='ward')
    fig,ax = plt.subplots(figsize=(8,6))
    
    # plt.figure(figsize=(10,8))
    dendrogram(Z, labels = campaign_df['campaign'].values)

    return fig, ax
    # plt.title('Campaign Clusters')
    # plt.xticks(rotation=45)
    # plt.show()

# standardize numerical columns
def get_clusters(campaign_df):
    """perform KMeans and project down using PCA to get most valuable information
    across the three features. 

    Args:
        campaign_df (Pandas.DataFrame): A DataFrame with monthly average crowd 
        levels, absolute, and relative marketing lift from each campaign in a 
        specific theme park

    Returns:
        (matplotlib.figure.Figure, matplotlib.axes._axes.Axes): A fig, ax object 
        holding the plot for KMeans projected down using PCA. 
    """
    print(campaign_df.head(5))
    
    # obtain numerical features
    X = campaign_df[['avg_crowd_campaign_month', 'absolute_lifts', 'relative_lifts']]
    
    # scale numerical features to ensure equal representation of each feature
    X_scaled = StandardScaler().fit_transform(X)

    # fit and assign cluster labels to each campaign  
    kmeans_model = KMeans(n_clusters=2, random_state=731).fit(X_scaled)
    campaign_df['cluster'] = kmeans_model.labels_

    # visualise using PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    # assign principle component values to each campaign
    campaign_df['First PC'], campaign_df['Second PC'] = X_pca[:,0], X_pca[:, 1]

    fig, ax = plt.subplots(figsize=(8,6))
    colors = ['mediumseagreen', 'red']

    components = pca.components_

    # To obtain the principle component weights
    for i, component in enumerate(components, 1):
        print(f"Principal Component {i} weights:")
        print(component)

    # observe the explained variance of each principle component to see the 
    # proportion of information explained from each axis
    # print(f"\nExplained Variance Ratio (%):{pca.explained_variance_ratio_}")
        
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

    #plt.title('Campaign Clusters (KMeans Clustering, PCA Visualisation)')    
    plt.text(0.5, -0.15, 'Figure 1: Campaign Clusters (KMeans Clustering, PCA Visualisation)', 
         ha='center', va='center', transform=ax.transAxes, fontsize=10)
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.legend()
    # plt.show()

    # ensure that values are rounded
    return (fig, ax, np.round(components, decimals=2), np.round(pca.explained_variance_ratio_, 2))         
    

# Tron Light Cycle Run
lift1 = get_lift_of_campaign(df_crowd, 'Disney Magic Kingdom', '2023-03-01')

# Journey Of Water
lift2 = get_lift_of_campaign(df_crowd, 'Epcot', '2023-10-01')

# Fantasy Spring
lift3 = get_lift_of_campaign(df_crowd, 'Tokyo DisneySea', '2023-12-01')

# Dreamworks Land
lift4= get_lift_of_campaign(df_crowd, 'Universal Studios At Universal Orlando', '2023-12-01')  

      
# Freight Fest
lift5 =get_lift_of_campaign(df_crowd, 'Six Flags Great America', '2024-08-01')      

# Pipeline: The Surf Coaster
lift6= get_lift_of_campaign(df_crowd, 'Seaworld Orlando', '2023-05-01')      

# Dino Valley
lift7= get_lift_of_campaign(df_crowd, 'Legoland California', '2024-03-01')

# prepare desired campaigns
theme_parks = ['Magic Kingdom', 'Epcot', 'Tokyo DisneySea', \
    'Universal Studios At Universal Orlando', 'Six Flags Great America',\
    'Seaworld Orlando', 'Legoland California']
campaign = ['Tron Light Cycle Run', 'Jouney Of Water', 'Fantasy Spring', \
    'DreamWorks Land', 'Freight Fest', 'Pipeline: The Surf Coaster', \
    'Dino Valley']
all_lifts = [lift1, lift2,lift3, lift4, lift5, lift6, lift7]
absolute_lifts = [lift[0] for lift in all_lifts]
relative_lifts = [lift[1] for lift in all_lifts]
avg_crowd_campaign_month = [lift[2] for lift in all_lifts]

# obtain monthly time series data of desired campaigns
campaign_df = pd.DataFrame({'theme_parks':theme_parks, 'campaign':campaign, \
    'avg_crowd_campaign_month':avg_crowd_campaign_month, \
    'absolute_lifts':absolute_lifts, 'relative_lifts': relative_lifts})

# get_clusters(campaign_df)