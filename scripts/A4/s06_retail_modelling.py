#####################################
# author: Chris Yong Hong Sen
# date: 02 Apr 2025
# preamble: Find best K for KMeans; Fitting KMeans and visualing
#
# pre-req: KMeans Algorithm; basic pandas manipulations
#
# additional notes: df_labelled and get_kmeans_labels() function is used in 
#                   streamlit page in ../../pages/A4.py
#           
######################################

import pandas as pd
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer 
import plotly.express as px

# read in transformed data
df = pd.read_csv('../data/clean/rmf.csv')

################################################
#                                              #
#               FIND BEST K                    #
#                                              #
################################################
def determine_optimal_k(df):
    # ensure initiate everytime we call the function to ensure reproducibility
    model = KMeans(random_state=734)
    
    # initiate the KElbowVisualizer
    visualizer = KElbowVisualizer(model, k=(2,10))

    # fit the KElbowVisualizer
    visualizer.fit(df)
    
    # # save the plot
    # visualizer.show(outpath='../other/static_plot/optimal_k_means.jpg') # UNCOMMENT
    
    return visualizer
    
    # plot graph
    # visualizer.show()

################################################
#                                              #
#               FIT BEST KMEANS                #
#                                              #
################################################

def get_kmeans_labels(df):
    
    # reinitiate to ensure reproducibility
    model = KMeans(n_clusters=4, random_state=734)
    model.fit_transform(df)

    # label each observation with their nearest centroid
    df['cluster'] = model.labels_

    # determine natura of each cluster
    cluster_groups = df.groupby('cluster').agg('mean')
    feature_ranks = cluster_groups.rank(ascending=True, method='first')
    feature_ranks['Score'] = feature_ranks.sum(axis=1)
    print(cluster_groups)
    
    # observe cluster_groups and feature_ranks.
    # 
    #      Champions       (2) - Highest F, M, and lowest R
    #       At Risk        (0) - Second highest F, M, and third lowest R 
    # Potential Loyalists  (3) - Third highest F, M, and second lowest R  
    #     Hibernating    (1) - Fourth highest F, M, and fourth lowest R
    #
    #
    # NOTE: We want high frequency and monetary, and low recency 
    
    label = ['At Risk', 'Hibernating', 'Champions', 'Potential Loyalists']
    cluster_groups['Label'] = label
    df['Segment'] = df['cluster'].apply(lambda cluster: cluster_groups.loc[cluster].get('Label'))

    return df

def plot_3d_clusters(df_labelled):
    fig = px.scatter_3d(
        df_labelled,
        x='Recency',
        y='Frequency',
        z='Monetary',
        color='Segment',
        hover_name='CustomerID',
        symbol='Segment',
        opacity=0.7,
        title='<b>RFM KMeans Clusters</b>',
        labels={'Recency':"Days since company's most recent transaction",
                'Frequency': 'Total transactions',
                'Monetary': 'Total Spending ($)'},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    fig.update_layout(
        scene={
            'xaxis': {'title_font': {'size': 14}},
            'yaxis': {'title_font': {'size': 14}},
            'zaxis': {'title_font': {'size': 14}}},
        margin={'l':0, 'r':0, 'b':0, 't': 40},
        legend={'orientation':'h', 'yanchor':'bottom'}
    )
    
    # # save figure
    # fig.write_html('../other/interactive_plot/guest_segmentation_clusters.html') #UNCOMMENT
    
    
    return fig
    # plot
    # fig.show()


################################################
#                                              #
#             COMBINED WORKFLOR                #
#                                              #
################################################

# # Using elbow method, best K is 4
# determine_optimal_k(df) # UNCOMMENT

# run kmeans and label each observation to their centroids, 
df_labelled = get_kmeans_labels(df.iloc[:,1:]) # don't fit on CustomerID
df_labelled['CustomerID'] = df['CustomerID']   # relabel CustomerID

# plot_3d_clusters(df_labelled) 
