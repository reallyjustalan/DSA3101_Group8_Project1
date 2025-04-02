import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_disney_attendance_data(filepath="data/A5/cleaned_disney_attendance.csv"):
    return pd.read_csv(filepath)

def load_reviews_data(filepath="data/A5/cleaned_DisneylandReviews.csv"):
    return pd.read_csv(filepath)

def merged_disney(attendance_disney, DisneylandReviews_data):
    """Merge attendance and review data, shifting ratings by one year to check if previous year ratings affects attendance."""
    avg_rating_per_park_year = DisneylandReviews_data.groupby(["Branch", "Year"])["Rating"].mean().reset_index()

    # Merge attendance_disney and avg_rating_per_park_year on "Park" and "Year"
    merged_df = pd.merge(attendance_disney, avg_rating_per_park_year, 
                          left_on=["Park", "Year"], right_on=["Branch", "Year"], how="outer")

    # Drop duplicate column
    merged_df.drop(columns=["Branch"], inplace=True)

    # Shift ratings by 1 year
    merged_df["Prev_Year_Rating"] = merged_df.groupby("Park")["Rating"].shift(1)

    # Drop rows where previous year's rating is NaN (first year has no previous year)
    merged_df = merged_df.dropna()

    return merged_df

def correlation_plot(merged_df):
    """Plot the correlation between previous year's rating and attendance."""
    correlation = merged_df["Prev_Year_Rating"].corr(merged_df["Attendance"])
    print(correlation)
    
    plt.figure(figsize=(8, 5))
    sns.regplot(x=merged_df["Prev_Year_Rating"], y=merged_df["Attendance"])
    plt.xlabel("Previous Year's Rating")
    plt.ylabel("Current Year's Attendance")
    plt.title("Impact of Previous Year's Rating on Attendance")

    return plt

# The correlation value of 0.525 suggests that there is a moderate positive relationship between 
# previous year ratings and next year's attendance.