import streamlit as st 
import pandas as pd


st.title("Disneyland Reviews Coded Data")
st.write("This is the coded data from the Disneyland reviews.")

df_coded = pd.read_csv("data/A1/DisneylandReviews_Coded.csv")
df_sample = pd.read_csv("data/A1/DisneylandReviews_Sample.csv")

df_sample = df_sample.rename(columns={'Review_ID': "review_id"})

merged_df = pd.merge(df_sample, df_coded, on="review_id")

merged_df["touchpoint_sentiment"] = merged_df["touchpoint"] + "_" + merged_df["sentiment"]

df_pivot = (
    merged_df.groupby(["review_id", "touchpoint_sentiment"])
      .size()
      .unstack(fill_value=0)
      .reset_index()
)

review_info = merged_df[["review_id", "Rating", "Branch"]].drop_duplicates(subset=["review_id"])
df_analysis = pd.merge(df_pivot, review_info, on="review_id", how="left")
df_analysis

# Select only numeric columns (counts and rating)
numeric_df = df_analysis.select_dtypes(include="number")

# Compute the correlation matrix
corr_matrix = numeric_df.corr(method="pearson")

# Look at how each touchpoint-sentiment correlates with Rating
corr_with_rating = corr_matrix["Rating"].sort_values(ascending=False)
corr_with_rating


