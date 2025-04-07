import pandas as pd
from A2_dataprocessing import load_and_clean_data
from A2_createplots import create_plots
from A2_DBSCAN import DBSCANmodel
from A2_KMeans_all import KM_all
from A2_KMeansContinent import KMContinent
from A2_Mismatch import mm
from A2_KMeansVisit import KMVisit
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "../../data/A2/updated_disneylandreviews.csv")
df = load_and_clean_data(csv_path)

df_all = df
df_hongkong = df[df['Branch'] == 'Disneyland_HongKong']
df_california = df[df['Branch'] == 'Disneyland_California']
df_paris = df[df['Branch'] == 'Disneyland_Paris']

# Create the plots for the exploratory Data analysis
create_plots(df_all, df_hongkong, df_california, df_paris)

# First model, which used DBSCAN to cluster the guests
DBSCANmodel(df_all)

# Second model, which used KMeans to cluster the guests
KM_all(df_all)

# Third Model, used KMeans to do Mismatch Analysis
mm(df_all)

# Fourth Model, Split data to group the guest based on continent, then cluster
KMContinent(df_all)

# Fifth Model, Split data to group the guest based on Visit_Type, then cluster
KMVisit(df_all)