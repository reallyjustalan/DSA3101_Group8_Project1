import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Check which months on average have better sentiment scores and ratings

#Sentiment rated from 0 to 1
#Sentiments were mostly constant throughout the months with the highest being 0.706328 in November
#lowest being 0.652312 in August
def monthly_sentiment_scores(DisneylandReviews_data):
    monthly_sentiment = DisneylandReviews_data.groupby("Month")["Sentiment_Score"].mean().reset_index()
    print(monthly_sentiment)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=monthly_sentiment["Month"], y=monthly_sentiment["Sentiment_Score"])

    plt.xlabel("Month")
    plt.ylabel("Average Sentiment")
    plt.title("Average Sentiment by Month")
    plt.xticks(range(12), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    return plt

#Ratings from 0 to 5
#Ratings were mostly constant throughout the months with the highest being 4.362229 in September
#lowest being 4.115423 in August

def monthly_rating_scores(DisneylandReviews_data):
    monthly_ratings = DisneylandReviews_data.groupby("Month")["Rating"].mean().reset_index()
    print(monthly_ratings)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=monthly_ratings["Month"], y=monthly_ratings["Rating"])

    plt.xlabel("Month")
    plt.ylabel("Average Rating")
    plt.title("Average Ratings by Month")
    plt.xticks(range(12), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    return plt


#Line plot of ratings for all years and month for each park

def lineplot_ratings_all(DisneylandReviews_data):
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
    ratings_trend = DisneylandReviews_data.groupby(["Branch", "Year", "Month"])["Rating"].mean().reset_index()
    branches = ratings_trend["Branch"].unique()

    for branch in branches:
        plt.figure(figsize=(10, 6))
        branch_data = ratings_trend[ratings_trend["Branch"] == branch].pivot(index="Year", columns="Month", values="Rating")

        # Define a consistent color range from 0 to 5
        sns.heatmap(branch_data, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5, vmin=0, vmax=5)
        
        plt.xlabel("Month")
        plt.ylabel("Year")
        plt.title(f"Heatmap of Ratings for {branch}")
        return plt

def heatmap_month_branch_ratings():
    ratings_trend = DisneylandReviews_data.groupby(["Branch", "Year", "Month"])["Rating"].mean().reset_index()
    monthly_avg_ratings = ratings_trend.groupby(["Branch", "Month"])["Rating"].mean().reset_index()

    # Get the unique branches
    branches = monthly_avg_ratings["Branch"].unique()

    # Plot a heatmap for each branch
    for branch in branches:
        plt.figure(figsize=(10, 6))
        
        # Filter data for the current branch
        branch_data = monthly_avg_ratings[monthly_avg_ratings["Branch"] == branch].pivot(index="Month", columns="Branch", values="Rating")

        # Define a consistent color range from 0 to 5
        sns.heatmap(branch_data, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5, vmin=0, vmax=5)

        plt.xlabel("Branch")
        plt.ylabel("Month")
        plt.title(f"Average Monthly Ratings for {branch}")
        plt.show()

def heatmap_sentiments(DisneylandReviews_data):
    sentiment_trend = DisneylandReviews_data.groupby(["Branch", "Year", "Month"])["Sentiment_Score"].mean().reset_index()
    branches = sentiment_trend["Branch"].unique()

    for branch in branches:
        plt.figure(figsize=(10, 6))
        branch_data = sentiment_trend[sentiment_trend["Branch"] == branch].pivot(index="Year", columns="Month", values="Sentiment_Score")

        # Define a consistent color range from 0 to 5
        sns.heatmap(branch_data, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5, vmin=0, vmax=1)
        
        plt.xlabel("Month")
        plt.ylabel("Year")
        plt.title(f"Heatmap of Sentiments for {branch}")
        return plt