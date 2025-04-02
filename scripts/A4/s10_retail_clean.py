#################################
#
#   GOAL: clean missing values
#
#      1A - Description NA values (0.27% of total observations) DROP
#      1B - CustomerID NA values (~25% of total observations) DROP
#      1C - Cancellation orders (1.71% of total observations) DROP
#      1D - Quantity negative values (~0% of total observations) DROP
#      1  - TOTAL 26.58% dropped
#
#   NOTE: We can safely drop 1A, 1C, and 1D since they account for less than a 
#         hundredth of the overall sampling population. For 1C, we consider the 
#         fact that For subsequent RMF analysis, we require unique customerID,
#         therefore we have to remove missing customer IDs despite high 
#         representative of missing values compared to overall sample. The final
#         dataset will be composed of 
#
#################################
import numpy as np
import pandas as pd

# read in data
retail_data = pd.read_csv('data/A4/raw/retail.csv').iloc[:,1:8]

def explore_df_general_na(retail_data):
    # obtain number of missing values per feature
    missing_val_per_column = retail_data.isnull().sum()
    print('\noverall missing values\n')
    print(missing_val_per_column)

    print('---------------------------------------')
    print('\n\nMissing values in \'Description Column\'\n')

# 'Description' feature missing values 
def explore_description_na(retail_data):
    col_description_NA_df = retail_data[retail_data['Description'].isnull()]
    print(col_description_NA_df.head(5))

    desc_total_missing = col_description_NA_df['Description'].isnull().sum() 
    prop_of_missing_descriptions = round(desc_total_missing/retail_data.shape[0]*100, 2) 
    print(f'\n\nprop of missing data from description col: {prop_of_missing_descriptions}%')
    print('---------------------------------------')



# 'CustomerID' feature missing values
def explore_custid_na(retail_data):
    print('---------------------------------------')
    print('\n\nMissing values in \'CustomerID Column\'\n')
    custID_NA_df = retail_data[retail_data['CustomerID'].isnull()]
    print(custID_NA_df.head(5))

    custID_total_missing = custID_NA_df['CustomerID'].isnull().sum() 
    prop_of_missing_custID = round(custID_total_missing/retail_data.shape[0]*100, 2) 
    print(f'\n\nprop of missing data from CustomerID col: {prop_of_missing_custID}%')
    print('---------------------------------------\n')


# 'Quantity' negative values
# CASE 1: invoice starts w 'C' for negative 'Quantity'
# CASE 2: invoice starts w '5' for negative 'Quantity'
def explore_quantity_na(retail_data):
    cond = (retail_data['Quantity'] <= 0)
    refund_df = retail_data[cond]

    # All refunded transactions start with 'C' or '5'
    unique_refund_start_df = refund_df['InvoiceNo'].str[0].value_counts()
    start_chars = unique_refund_start_df.index.to_list()

    # CASE 1: 'C' Invoice transactions are expected returns given Description 
    focused_cols = ['InvoiceNo', 'Description', 'Quantity']
    refund_c = refund_df[refund_df['InvoiceNo'].str.startswith(start_chars[0])][focused_cols]
    print('---------------------------------------')
    print('\n"C" InvoiceNo refunded transactions\n')
    print(refund_c.head(5))

    print('\nCount of unique "C" InvoiceNo\n')
    grouped_refund_c = refund_c['InvoiceNo'].value_counts()  
    prop_refunded_c = round(grouped_refund_c.sum()/retail_data.shape[0]*100,2)

    print(grouped_refund_c)
    print(f'\nTotal unique "C" Invoice: {len(grouped_refund_c.index)}')
    print(f'Total "C" Invoice: {grouped_refund_c.sum()}\n')
    print(f'Prop Invoice: {prop_refunded_c}%\n')
    print('---------------------------------------')

    # CASE 2: Refund transactions starting with '5' has too many missing information
    # Since there are only two UnitPrice which are negative, we can safely remove 
    # these observation from our analysis.
    print(refund_df[refund_df['InvoiceNo'].str.startswith(start_chars[1])][['Description', 'Quantity']])


# 'UnitPrice' negative values: simply remove since only 2 observations 
def explore_unitprice_na(retail_date):
    negative_price_df = retail_data[retail_data['UnitPrice'] < 0]
    print('-------------------------------------------')
    print('\nObservations with negative (-) UnitPrice\n')
    print(retail_data[retail_data['UnitPrice'] == min(retail_data['UnitPrice'])])

    print('\nunique negative UnitPrices\n')
    print(negative_price_df['UnitPrice'].value_counts())
    print('\n-------------------------------------------')

def explore_na_thoroughly(retail_data):
    explore_df_general_na(retail_data)
    explore_description_na(retail_data)
    explore_custid_na(retail_data)
    explore_quantity_na(retail_data)
    explore_unitprice_na(retail_data)
    
#######################
#######################

# Final Cleaning Script: Remove 1A to 1D
def clean_retail_data(retail_data):
    cleaning_cond = (retail_data['Quantity'] > 0) & \
        (retail_data['UnitPrice'] > 0) & \
        (~retail_data['CustomerID'].isnull())
        
    clean_data = retail_data[cleaning_cond]
    relative_drop = (clean_data.shape[0] - retail_data.shape[0])/retail_data.shape[0] 
    perc_drop = round(relative_drop*100, 2)
    print(f'\nTotal number of missing values per col\n')
    print(clean_data.isnull().sum())
    print(f'\nTotal percentage observations dropped: {perc_drop}%\n')
    return clean_data

clean_data = clean_retail_data(retail_data)

# save clean data for further analysis
# clean_data.to_csv('../data/clean/retail_analysis.csv', index=False)