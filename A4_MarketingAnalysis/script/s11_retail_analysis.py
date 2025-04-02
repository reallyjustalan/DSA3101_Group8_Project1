#################################
#
#   GOAL: preprocess for k-means
#
#   NOTE: Since k-means is a distance based algorithm, we have to ensure that 
#         all numerical variable are scaled and categorical variables are 
#         one-hot encoded
#
#################################
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.stats import gaussian_kde
from sklearn.preprocessing import StandardScaler

# read in clean data
df = pd.read_csv('../data/analysis/retail_analysis.csv')

################################################
#                                              #
#               PREPROCESSING 1                #
#                                              #
################################################

def preprocess_clean_data(df, categorical_var = ['CustomerID','Description', \
                                                    'StockCode', 'InvoiceNo']):
    # observe the incorrect data types
    # print(df.info()) #UNCOMMENT TO CHECK

    # change to correct data type
    df[categorical_var] = df[categorical_var].astype('category')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # verify data type is correct
    # print(df.info()) #UNCOMMENT TO CHECK
    # print(df.select_dtypes('number')) #UNCOMMENT TO CHECK


    # PREPROCESSING 1A: get total cost of transaction
    df['TransactionalTotal'] = df['Quantity'] * df['UnitPrice']   


    # PREPROCESSING 1B: RMF Framework
    #                       
    #      Recency   - How *recently a patron performed the transaction      
    #      Frequency - How *often a patron performed the transaction
    #      Monetary  - How *much a patron spends on their transactions
    #
    # NOTE: RMF framworks ranks patrons from 1 to 5 in each of these categories
    #       Better customers would have higher scores across all three categories.
    #       Also note that this framework heavily weights recent purchases as we 
    #       assume that a patron who had recently made a transaction is more likely
    #       to make another transaction compared to a patron who havent made a 
    #       transaction for a longer period of time (eg a year since last purchase) 


    # the last transaction's date will be used as an anchor to measure Recency
    last_transaction_date = df['InvoiceDate'].max() + pd.DateOffset(days=1)

    rmf_df = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda date: (last_transaction_date - date.max()).days,
        'CustomerID': 'count',
        'TransactionalTotal': 'sum' 
    })
    rename_func = {'InvoiceDate': 'Recency', 
                'CustomerID': 'Frequency',
                'TransactionalTotal': 'Monetary'}
    rmf_df = rmf_df.rename(rename_func, axis=1)

    return rmf_df



################################################
#                                              #                                              #
#               EXPLORATION                    #
#                                              #
################################################

# plot histogram with KDE density plot overlaid
def plot_histogram(rmf_df, feature, smoothing_kernals):
    
    # Use Kernal Density Estimation in preparation for density curve overlay
    kde = gaussian_kde(rmf_df[feature], bw_method=0.4)
    x_grid = np.linspace(rmf_df[feature].min()-5, rmf_df[feature].max()+5, smoothing_kernals)
    binsize = (rmf_df[feature].max() - rmf_df[feature].min())/50    
    
    y_kde = kde(x_grid) * len(rmf_df) * binsize
    # y_kde = kde(x_grid) * len(rmf_df) * (rmf_df[feature].max() -rmf_df[feature].min())/12
    
    
    # plot histogram
    fig = px.histogram(rmf_df, 
                    x=feature, 
                    opacity=0.7,
                    nbins=50,
                    histnorm=None)

    fig.add_trace(px.line(x=x_grid,y=y_kde).data[0].update(
        line={'color': 'red',
              'width': 3},
        name='Density',
        hovertemplate='Average Count'
    ))
    
    fig.update_traces(marker={'line': {'width':1.5,'color':'darkblue'}})
    fig.update_layout(width=800, 
                    height=600,
                    autosize=False,
                    title={'text':f'Histogram of {feature}',
                            'y': 0.95,
                            'x': 0.5,
                            'font':{'size':20}}, 
                    xaxis={'tickangle': -45,
                            'title': feature},
                    yaxis={'title':'Count'},
                    showlegend=True)
    fig.show()
    
# all three plots are severely right skewed. If left in this skewed state,
# KMeans model would be highly bias. This motivates the need for a log 
# transformation

# plot_histogram(rmf_df,'Recency', 500)
# plot_histogram(rmf_df, 'Frequency', 500)
# plot_histogram(rmf_df, 'Monetary', 500)





################################################
#                                              #
#               PREPROCESSING 2                #
#                                              #
################################################

# apply log transformation (apply +1 to prevent '0' approaching negative inf)
def account_for_skew(rmf_df):
    rmf_transformed = rmf_df.apply(lambda x: np.log(x+1), axis=1)
    return  rmf_transformed
# we can immediately see distribution of 
# plot_histogram(rmf_transformed, 'Recency', 200)
# plot_histogram(rmf_transformed, 'Frequency', 200)
# plot_histogram(rmf_transformed, 'Monetary', 200)

# we can see that despite applying log transformation, Monetary has double the mean 
# comapred to Recency and Frequency, and because KMeans is a distance-based
# algorithm, Monetary would be the dominating feature in determining clusters
# therefore, we will be standardizing the values.
def account_for_feature_diff(rmf_df):
    scaler = StandardScaler()    
    rmf_transformed = scaler.fit_transform(rmf_df)
    
    return  pd.DataFrame(rmf_transformed,columns= rmf_df.columns, index=rmf_df.index)

################################################
#                                              #
#             COMBINED WORKFLOR                #
#                                              #
################################################

# obtain Recency, Frequency, Monetary features
rmf_df = preprocess_clean_data(df)

# log-scale to address severe right skew and feature distance difference
rmf_transformed = account_for_skew(rmf_df)
rmf_transformed = account_for_feature_diff(rmf_transformed)

# # save pre-processed data
# rmf_transformed.to_csv('../data/clean/rmf.csv', index=True) # UNCOMMENT









