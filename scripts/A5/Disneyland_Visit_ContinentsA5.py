import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Continent of Origin and Month of Visit 
#People from North America and Europe tend to leave the most reviews consistently.
def continent_month_plot(DisneylandReviews_data):
    grouped = DisneylandReviews_data.groupby(["Continent", "Month"]).size().reset_index(name="Review_Count")

    # Pivot the data for heatmap
    pivot = grouped.pivot(index="Continent", columns="Month", values="Review_Count")

    # Create the heatmap
    sns.heatmap(pivot, cmap="coolwarm", annot=True, fmt="g")  # fmt="g" ensures proper integer formatting

    plt.title("Reviews by Continent and Month")
    return plt

#Visit type and Month of Visit
# Based on the reviews, most people travel with their family with June to August, 
# October and December being the popular months. This is in line with school holidays such a 
# Summer and Winter break. Guest going with their families tend to give the most reviews

def visit_type_month(DisneylandReviews_data):
    grouped = DisneylandReviews_data.groupby(["Visit_Type", "Month"]).size().reset_index(name="Review_Count")

    # Create a pivot table
    pivot = grouped.pivot(index="Visit_Type", columns="Month", values="Review_Count")

    # Display the pivot table
    print(pivot)

    # Line plot for trends
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=grouped, x="Month", y="Review_Count", hue="Visit_Type", marker="o")

    # Labels and title
    plt.xlabel("Month")
    plt.ylabel("Number of Reviews")
    plt.title("Trend of Visit Types Over Months")
    plt.legend(title="Visit Type")
    plt.grid(True)
    return plt


#Visit Type and Ratings/Sentiment Scores
#Families tend to give poor ratings

#Ratings
def visit_type_rating(DisneylandReviews_data):
    # Group by Visit Type and calculate average rating
    visit_type_rating = DisneylandReviews_data.groupby("Visit_Type")["Rating"].mean().reset_index()
    print(visit_type_rating)

    # Bar plot to visualize ratings by visit type
    plt.figure(figsize=(8, 5))
    sns.barplot(data=visit_type_rating, x="Visit_Type", y="Rating", palette="coolwarm")

    # Labels
    plt.xlabel("Visit Type")
    plt.ylabel("Average Rating")
    plt.title("Average Rating by Visit Type")
    plt.xticks(rotation=45)
    plt.ylim(0, 5)  # Ratings are between 1-5
    return plt

#Sentiment Score
def visit_type_sentiment(DisneylandReviews_data):
    # Group by Visit Type and calculate average rating
    visit_type_rating = DisneylandReviews_data.groupby("Visit_Type")["Sentiment_Score"].mean().reset_index()
    print(visit_type_rating)

    # Bar plot to visualize ratings by visit type
    plt.figure(figsize=(8, 5))
    sns.barplot(data=visit_type_rating, x="Visit_Type", y="Sentiment_Score", palette="coolwarm")

    # Labels
    plt.xlabel("Visit Type")
    plt.ylabel("Average Sentiment_Score")
    plt.title("Average Sentiment_Score by Visit Type")
    plt.xticks(rotation=45)
    plt.ylim(0, 1)  
    return plt

#Continent of Origin and Rating/Sentiment Score
def continent_rating(DisneylandReviews_data):
    # Group by Visit Type and calculate average rating
    continent_type_rating = DisneylandReviews_data.groupby("Continent")["Rating"].mean().reset_index()
    print(continent_type_rating)

    # Bar plot to visualize ratings by visit type
    plt.figure(figsize=(8, 5))
    sns.barplot(data=continent_type_rating, x="Continent", y="Rating", palette="coolwarm")

    # Labels
    plt.xlabel("Continent")
    plt.ylabel("Average Rating")
    plt.title("Average Rating by Continent")
    plt.xticks(rotation=45)
    plt.ylim(0, 5)  # Ratings are between 1-5
    return plt

def continent_sentiment(DisneylandReviews_data):
    # Group by Visit Type and calculate average rating
    continent_type_sentiment = DisneylandReviews_data.groupby("Continent")["Sentiment_Score"].mean().reset_index()
    print(continent_type_sentiment)

    # Bar plot to visualize ratings by visit type
    plt.figure(figsize=(8, 5))
    sns.barplot(data=continent_type_sentiment, x="Continent", y="Sentiment_Score", palette="coolwarm")

    # Labels
    plt.xlabel("Continent")
    plt.ylabel("Average Sentiment_Score")
    plt.title("Average Sentiment_Score by Continent")
    plt.xticks(rotation=45)
    plt.ylim(0, 1)  
    return plt

