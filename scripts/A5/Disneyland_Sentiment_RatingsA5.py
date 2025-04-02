import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Check which months on average have better sentiment scores and ratings

def load_reviews_data(filepath="data/A5/cleaned_DisneylandReviews.csv"):
    return pd.read_csv(filepath)

def monthly_sentiment_scores(DisneylandReviews_data):
    """
    Computes and visualizes average sentiment scores by month.
    Shows a bar plot showing the average sentiment score for each month.

    Sentiment rated from 0 to 1
    Sentiments were mostly constant throughout the months with the highest being 0.706328 in November
    lowest being 0.652312 in August
    """
    monthly_sentiment = DisneylandReviews_data.groupby("Month")["Sentiment_Score"].mean().reset_index()
    print(monthly_sentiment)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=monthly_sentiment["Month"], y=monthly_sentiment["Sentiment_Score"], palette="viridis")

    plt.xlabel("Month")
    plt.ylabel("Average Sentiment")
    plt.title("Average Sentiment by Month")
    plt.xticks(range(12), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    return plt


def monthly_rating_scores(DisneylandReviews_data):
    """
    Computes and visualizes average ratings by month.
    With A bar plot showing the average rating for each month.

    Ratings from 0 to 5
    Ratings were mostly constant throughout the months with the highest being 4.362229 in September
    lowest being 4.115423 in August
    """
    monthly_ratings = DisneylandReviews_data.groupby("Month")["Rating"].mean().reset_index()
    print(monthly_ratings)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=monthly_ratings["Month"], y=monthly_ratings["Rating"], palette="viridis")

    plt.xlabel("Month")
    plt.ylabel("Average Rating")
    plt.title("Average Ratings by Month")
    plt.xticks(range(12), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    return plt


#Line plot of ratings for all years and month for each park

def lineplot_ratings_all(DisneylandReviews_data):
    """
    Creates a line plot showing average ratings per month for each year and branch.
    Shows a facet grid with line plots of ratings by month for each branch.
    """
    ratings_trend = DisneylandReviews_data.groupby(["Branch", "Year", "Month"])["Rating"].mean().reset_index()

    g = sns.FacetGrid(ratings_trend, col="Branch", col_wrap=2, height=5, sharey=True)
    g.map_dataframe(sns.lineplot, x="Month", y="Rating", hue="Year", marker="o", palette="tab10")

    g.set_axis_labels("Month", "Average Rating")
    g.set_titles("{col_name}")  # Set branch name as title
    g.add_legend()

    plt.xticks(range(1, 13), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    return plt

#Heatmap to check rating and sentiment differences for each branch, 
# California and Hong Kong in general have higher ratings and sentiments.

def heatmap_ratings(DisneylandReviews_data):
    """
    Creates heatmaps displaying rating variations by year and month for each branch.
    Disneyland California has highest ratings followed by Hong Kong then Paris
    """
    ratings_trend = DisneylandReviews_data.groupby(["Branch", "Year", "Month"])["Rating"].mean().reset_index()
    branches = ratings_trend["Branch"].unique()

    figures = []  # Store figures for better display later

    for branch in branches:
        fig, ax = plt.subplots(figsize=(10, 6))  # Use fig, ax instead of plt.figure()
        branch_data = ratings_trend[ratings_trend["Branch"] == branch].pivot(index="Year", columns="Month", values="Rating")

        # Define a consistent color range
        sns.heatmap(branch_data, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5, vmin=0, vmax=5, ax=ax)

        ax.set_xlabel("Month")
        ax.set_ylabel("Year")
        ax.set_title(f"Heatmap of Ratings for {branch}")

        figures.append(fig)  # Store figure

    return figures  # Return list of figures

def heatmap_month_branch_ratings(DisneylandReviews_data):
    """
    Creates heatmaps displaying rating variations by month for each branch.
    Disneyland California has highest ratings followed by Hong Kong then Paris
    """
    ratings_trend = DisneylandReviews_data.groupby(["Branch", "Year", "Month"])["Rating"].mean().reset_index()
    monthly_avg_ratings = ratings_trend.groupby(["Branch", "Month"])["Rating"].mean().reset_index()

    branches = monthly_avg_ratings["Branch"].unique()
    figures = []  # Store figures

    for branch in branches:
        fig, ax = plt.subplots(figsize=(10, 6))  # Create figure and axis
        
        # Filter data for the current branch
        branch_data = monthly_avg_ratings[monthly_avg_ratings["Branch"] == branch].pivot(index="Month", columns="Branch", values="Rating")

        # Define a consistent color range
        sns.heatmap(branch_data, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5, vmin=0, vmax=5, ax=ax)

        ax.set_xlabel("Branch")
        ax.set_ylabel("Month")
        ax.set_title(f"Average Monthly Ratings for {branch}")

        figures.append(fig)  # Store figure

    return figures  # Return list of figures

def heatmap_sentiments(DisneylandReviews_data):
    """
    Creates heatmaps displaying sentiment score variations by year and month for each branch.
    """
    sentiment_trend = DisneylandReviews_data.groupby(["Branch", "Year", "Month"])["Sentiment_Score"].mean().reset_index()
    branches = sentiment_trend["Branch"].unique()

    figures = []  # Store figures for neater display

    for branch in branches:
        fig, ax = plt.subplots(figsize=(10, 6))  # Use fig, ax
        branch_data = sentiment_trend[sentiment_trend["Branch"] == branch].pivot(index="Year", columns="Month", values="Sentiment_Score")

        # Define a consistent color range
        sns.heatmap(branch_data, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5, vmin=0, vmax=1, ax=ax)

        ax.set_xlabel("Month")
        ax.set_ylabel("Year")
        ax.set_title(f"Heatmap of Sentiments for {branch}")

        figures.append(fig)  # Store figure

    return figures 