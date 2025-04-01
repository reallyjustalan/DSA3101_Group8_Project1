import ssl
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import holidays
from scipy.stats import ttest_ind
import pycountry_convert as pc
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import streamlit as st


#Read files
attendance_data = pd.read_csv("data/A5/cleaned_attendance.csv")
attendance_data["USAGE_DATE"] = pd.to_datetime(attendance_data["USAGE_DATE"])

attendance_disney = pd.read_csv("data/A5/cleaned_disney_attendance.csv")

DisneylandReviews_data = pd.read_csv("data/A5/cleaned_DisneylandReviews.csv")

#Tivoli and PortAventura Overview plot
def tivoli_PortAventura_overview(attendance_data):
    # Set up the plot
    plt.figure(figsize=(12, 6))

    # Plot attendance over time for each facility
    sns.lineplot(data=attendance_data, x="USAGE_DATE", y="attendance", hue="FACILITY_NAME", marker="o")

    # Beautify the plot
    plt.xlabel("Date")
    plt.ylabel("Attendance")
    plt.title("Attendance Over Time for Each Facility")
    plt.xticks(rotation=45)
    plt.legend(title="Facility Name")
    plt.grid(True)

    # Show the plot
    return plt

#Tivoli and PortAventura Monthly plot for each year
def tivoli_PortAventura_all_time(attendance_data):
    attendance_data["Year"] = attendance_data["USAGE_DATE"].dt.year
    attendance_data["Month"] = attendance_data["USAGE_DATE"].dt.month

    monthly_facility_mean = attendance_data.groupby(["Year", "Month", "FACILITY_NAME"])["attendance"].mean().reset_index()
    unique_years = monthly_facility_mean["Year"].unique()
    num_years = len(unique_years)

    fig, axes = plt.subplots(num_years, 1, figsize=(10, 5 * num_years), sharex=True, sharey=True)

    # Ensure axes is iterable even if there's only one year
    if num_years == 1:
        axes = [axes]

    # Plot each year separately
    for i, year in enumerate(sorted(unique_years)):
        ax = axes[i]
        subset = attendance_data[attendance_data["Year"] == year]  # Filter data for the current year

        sns.lineplot(data=subset, x="Month", y="standardized_attendance", hue="FACILITY_NAME", marker="o", ax=ax)

        ax.set_title(f"Attendance Trend for {year}")
        ax.set_xticks(range(1, 13))  # Ensure all months 1-12 appear on x-axis
        ax.set_xlabel("Month")
        ax.set_ylabel("standardized_attendance")
        ax.legend(title="Facility Name")

    return plt

#Shows counts of which day has the highest attendance per month and year
def tivoli_PortAventura_weekly_trend_max(attendance_data):
    max_attendance_per_month = attendance_data.groupby(["Year", "Month", "FACILITY_NAME"])["attendance"].max().reset_index()
    max_attendance_dates =  attendance_data.merge(max_attendance_per_month, on=["Year", "Month", "attendance"], how="inner")

    #plot day distribution
    # Count occurrences of each day in the max attendance dataset
    plt.figure(figsize=(10, 6))
    sns.countplot(data=max_attendance_dates, x="Day_of_Week", order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    # Customize the plot
    plt.xlabel("Day of the Week", fontsize=12)
    plt.ylabel("Count of Maximum Attendance Days", fontsize=12)
    plt.title("Distribution of Days with Maximum Attendance per Month", fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    return plt

#Shows mean attendance trend for each day
def tivoli_PortAventura_weekly_trend_mean(attendance_data):
    # Group data by Day_of_Week and calculate mean attendance
    mean_attendance_per_day = attendance_data.groupby("Day_of_Week", as_index=False)["attendance"].mean()
    mean_attendance_per_day.rename(columns={"attendance": "mean_attendance"}, inplace=True)

    # Define the correct day order
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Convert 'Day_of_Week' to a categorical variable with the correct order
    mean_attendance_per_day["Day_of_Week"] = pd.Categorical(
        mean_attendance_per_day["Day_of_Week"], categories=day_order, ordered=True
    )

    # Sort data by ordered days
    mean_attendance_per_day = mean_attendance_per_day.sort_values("Day_of_Week")

    # Set figure size
    plt.figure(figsize=(10, 6))

    # Create bar plot
    sns.barplot(
        data=mean_attendance_per_day,
        x="Day_of_Week",
        y="mean_attendance",
        order=day_order
    )

    plt.xlabel("Day of the Week", fontsize=12)
    plt.ylabel("Mean Attendance", fontsize=12)
    plt.title("Mean Attendance for Each Day of the Week", fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    return plt

def port_aventura_holidays_stat_test(attendance_data):

    plt.figure(figsize=(10, 6))
    portaventura_df = attendance_data[attendance_data["FACILITY_NAME"] == "PortAventura World"]
    spain_holidays = holidays.Spain(years=[2018, 2019, 2020, 2021, 2022])
    portaventura_df["is_holiday"] = portaventura_df["USAGE_DATE"].apply(lambda x: x in spain_holidays)

    #Check average attendance on holidays
    holiday_attendance = portaventura_df[portaventura_df["is_holiday"] == True]["attendance"].mean()
    non_holiday_attendance = portaventura_df[portaventura_df["is_holiday"] == False]["attendance"].mean()

    print(f"Average attendance on holidays: {holiday_attendance}")
    print(f"Average attendance on non-holidays: {non_holiday_attendance}")

    #Use T-test and p value to see if it is statistically significant
    holiday_values = portaventura_df[portaventura_df["is_holiday"] == True]["attendance"]
    non_holiday_values = portaventura_df[portaventura_df["is_holiday"] == False]["attendance"]

    t_stat, p_value = ttest_ind(holiday_values, non_holiday_values, equal_var=False)

    print(f"T-statistic: {t_stat}, P-value: {p_value}") #p-value less than 0.05, statistically significant

    #Plot
    sns.boxplot(x=portaventura_df["is_holiday"], y=portaventura_df["attendance"])
    plt.xlabel("Public Holiday")
    plt.ylabel("Attendance")
    plt.title("Park Attendance on Public Holidays vs. Non-Holidays")

    return plt

def port_aventura_holidays_plot(attendance_data):

    portaventura_df = attendance_data[attendance_data["FACILITY_NAME"] == "PortAventura World"]
    spain_holidays = holidays.Spain(years=[2018, 2019, 2020, 2021, 2022])
    portaventura_df["is_holiday"] = portaventura_df["USAGE_DATE"].apply(lambda x: x in spain_holidays)
    spain_holidays = holidays.Spain(years=portaventura_df["Year"].unique())

    # Select specific major holidays
    key_holidays = {
        "New Year's Day": "01-01",
        "Epiphany": "01-06",
        "Easter Sunday": "variable",
        "Labor Day": "05-01",
        "Christmas Day": "12-25"
    }

    # Convert variable holidays like Easter Sunday
    key_holidays["Easter Sunday"] = [date for date in spain_holidays if "Easter Sunday" in spain_holidays.get(date)]

    def get_holiday(date):
        date_str = date.strftime("%m-%d")
        for holiday, value in key_holidays.items():
            if isinstance(value, list) and date in value:
                return holiday
            elif date_str == value:
                return holiday
        return "Non-Holiday"

    portaventura_df["holiday_name"] = portaventura_df["USAGE_DATE"].apply(get_holiday)

    holiday_attendance = portaventura_df.groupby("holiday_name")["attendance"].mean().reset_index()
    print(holiday_attendance)

    #Plot
    plt.figure(figsize=(10, 5))
    sns.barplot(data=holiday_attendance, x="holiday_name", y="attendance", palette="viridis")

    plt.xlabel("Holiday")
    plt.ylabel("Average Attendance")
    plt.title("Park Attendance on Specific Holidays")
    plt.xticks(rotation=45)

    return plt

def tivoli_holidays_stat_test(attendance_data):
    plt.figure(figsize=(10, 6))
    tivoli_df = attendance_data[attendance_data["FACILITY_NAME"] == "Tivoli Gardens"]
    denmark_holidays = holidays.Denmark(years=[2018, 2019, 2020, 2021, 2022])
    tivoli_df["is_holiday"] = tivoli_df["USAGE_DATE"].apply(lambda x: x in denmark_holidays)

    #Check average attendance on holidays
    holiday_attendance = tivoli_df[tivoli_df["is_holiday"] == True]["attendance"].mean()
    non_holiday_attendance = tivoli_df[tivoli_df["is_holiday"] == False]["attendance"].mean()

    print(f"Average attendance on holidays: {holiday_attendance}")
    print(f"Average attendance on non-holidays: {non_holiday_attendance}")

    #Use T-test and p value to see if it is statistically significant
    holiday_values = tivoli_df[tivoli_df["is_holiday"] == True]["attendance"]
    non_holiday_values = tivoli_df[tivoli_df["is_holiday"] == False]["attendance"]

    t_stat, p_value = ttest_ind(holiday_values, non_holiday_values, equal_var=False)

    print(f"T-statistic: {t_stat}, P-value: {p_value}") #p-value less than 0.05, statistically significant

    #Plot
    sns.boxplot(x=tivoli_df["is_holiday"], y=tivoli_df["attendance"])
    plt.xlabel("Public Holiday")
    plt.ylabel("Attendance")
    plt.title("Park Attendance on Public Holidays vs. Non-Holidays")
    return plt

def tivoli_holidays_plot(attendance_data):
    tivoli_df = attendance_data[attendance_data["FACILITY_NAME"] == "Tivoli Gardens"]
    denmark_holidays = holidays.Denmark(years=[2018, 2019, 2020, 2021, 2022])
    tivoli_df["is_holiday"] = tivoli_df["USAGE_DATE"].apply(lambda x: x in denmark_holidays)

    denmark_holidays = holidays.Denmark(years=tivoli_df["Year"].unique())

    # Select specific major holidays
    key_holidays = {
        "New Year's Day": "01-01",
        "Easter Sunday": "variable",
        "Great Prayer Day": "variable",
        "Ascension Day": "variable",
        "Constitution Day": "06-05",
        "Christmas Eve": "12-24",
        "Christmas Day": "12-25",
        "Boxing Day": "12-26"
    }

    # Convert variable holidays (e.g., Easter Sunday, Great Prayer Day)
    variable_holidays = {}

    for date, name in denmark_holidays.items():
        holiday_name = str(name)  # Convert holiday name to a string
        if any(h in holiday_name for h in ["Easter", "Great Prayer", "Ascension"]):
            variable_holidays[holiday_name] = date

    # Add variable holidays to key_holidays
    key_holidays.update(variable_holidays)

    def get_holiday(date):
        date_str = date.strftime("%m-%d")
        for holiday, value in key_holidays.items():
            if isinstance(value, list) and date in value:
                return holiday
            elif date_str == value:
                return holiday
        return "Non-Holiday"

    tivoli_df["holiday_name"] = tivoli_df["USAGE_DATE"].apply(get_holiday)

    holiday_attendance = tivoli_df.groupby("holiday_name")["attendance"].mean().reset_index()
    print(holiday_attendance)


    plt.figure(figsize=(10, 5))
    sns.barplot(data=holiday_attendance, x="holiday_name", y="attendance", palette="viridis")

    plt.xlabel("Holiday")
    plt.ylabel("Average Attendance")
    plt.title("Park Attendance on Specific Holidays (Denmark)")
    plt.xticks(rotation=45)

    return plt


#SENTIMENTS AND RATINGS functions

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

def heatmap_ratings(DisneylandReviews_data):
    ratings_trend = DisneylandReviews_data.groupby(["Branch", "Year", "Month"])["Rating"].mean().reset_index()
    branches = ratings_trend["Branch"].unique()

    figures = []  # Store figures

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

def heatmap_sentiments(DisneylandReviews_data):
    sentiment_trend = DisneylandReviews_data.groupby(["Branch", "Year", "Month"])["Sentiment_Score"].mean().reset_index()
    branches = sentiment_trend["Branch"].unique()

    figures = []  # Store figures

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

#Continent of Origin and Month of Visit
#People from North America and Europe tend to leave the most reviews consistently.
def continent_month_plot(DisneylandReviews_data):
    grouped = DisneylandReviews_data.groupby(["Continent", "Month"]).size().reset_index(name="Review_Count")
    # Pivot for heatmap
    pivot = grouped.pivot(index="Continent", columns="Month", values="Review_Count")
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))  # Increase figure size
    # Generate heatmap
    sns.heatmap(pivot, cmap="coolwarm", annot=True, fmt="g", annot_kws={"size": 8}, ax=ax)  # Reduce annotation font size
    # Adjust axis labels
    plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels
    plt.yticks(rotation=0)  # Keep y-axis labels horizontal
    plt.title("Reviews by Continent and Month", fontsize=14)
    return fig 


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

def merged_disney(attendance_disney, DisneylandReviews_data):
    avg_rating_per_park_year = DisneylandReviews_data.groupby(["Branch", "Year"])["Rating"].mean().reset_index()

    # Merge attendance_disney and avg_rating_per_park_year on "Park" and "Year"
    merged_df = pd.merge(attendance_disney, avg_rating_per_park_year, left_on=["Park", "Year"], right_on=["Branch", "Year"], how="outer")

    # Drop duplicate column
    merged_df.drop(columns=["Branch"], inplace=True)

    #Shift ratings by 1 year
    merged_df["Prev_Year_Rating"] = merged_df.groupby("Park")["Rating"].shift(1)

    # Drop rows where previous year's rating is NaN (first year has no previous year)
    merged_df = merged_df.dropna()

    return merged_df

def correlation_plot(merged_df):
    correlation = merged_df["Prev_Year_Rating"].corr(merged_df["Attendance"])
    print(correlation)

    plt.figure(figsize=(8, 5))
    sns.regplot(x=merged_df["Prev_Year_Rating"], y=merged_df["Attendance"])
    plt.xlabel("Previous Year's Rating")
    plt.ylabel("Current Year's Attendance")
    plt.title("Impact of Previous Year's Rating on Attendance")

    return plt

merged_df = merged_disney(attendance_disney, DisneylandReviews_data)

# Page config
st.set_page_config(
    page_title="Seasonality Demographics",
    page_icon="🍁",
    layout="wide"
)

# Header
st.title("🍁 Seasonality Demographics")
st.write("How does seasonality, public holidays and visitor demographics impact theme park attendance and reviews?")


# Side bar
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose a section", ["Periodic Trends", "Sentiment and Ratings", "Visitor Demographics", "Ratings vs Attendance"])

if option == "Periodic Trends":
    st.header("Periodic Trends")
    st.markdown("In this section, we highlight the more significant periodic trends we have observed using attendance data from 2 theme parks, PortAventura World and Tivoli Gardens. We found that weekends and holidays have significantly higher attendance than other days as most people do not have to go to work or school and hence have the time to go to theme parks.")

    st.markdown("#### Overview")
    st.markdown("The Covid-19 pandemic which started in March 2020 and ended in May 2023 affected data within those years as shown in the dip in 2020 and saw 0 attendance for some periods in 2020 and 2021. It also took some time for attendance to increase to pre-pandemic levels.")
    st.pyplot(tivoli_PortAventura_overview(attendance_data))

    #st.markdown("#### Monthly Trend for each year")
    #st.markdown("Attendance from both parks follows the same trend roughly. Before Covid-19, summer break and winter break periods saw an increase in attendance.")

    #st.pyplot(tivoli_PortAventura_all_time(attendance_data))

    st.markdown("#### Daily Trend")
    st.markdown("The weekends have higher attendance with Saturday being the most popular day to visit the park.")
    st.pyplot(tivoli_PortAventura_weekly_trend_mean(attendance_data))

    st.markdown("#### Local events and holidays")
    st.markdown("Attendance on holidays are higher than on non-holidays. Among holidays, holidays such as Christmas and New Years are more popular times where people go to the parks.")
    st.markdown("##### PortAventura World (Spain)")
    st.markdown("PortAventura World which is in Spain sees higher attendance during Christmas, Labor Day and New Year's. The boxplot shows that the difference between holidays vs non-holidays is stastically significant. ")
    st.pyplot(port_aventura_holidays_stat_test(attendance_data))
    st.pyplot(port_aventura_holidays_plot(attendance_data))

    st.markdown("##### Tivoli Gardens (Denmark)")
    st.markdown("Tivoli Gardens which is in Denmark sees higher attendance during Christmas, Boxing Day and New Year's. The boxplot shows that the difference between holidays vs non-holidays is stastically significant. ")
    st.pyplot(tivoli_holidays_stat_test(attendance_data))
    st.pyplot(tivoli_holidays_plot(attendance_data))

elif option == "Sentiment and Ratings":
    st.header("Sentiment and Ratings")
    st.markdown("In this section, we highlight the different ratings and sentiments of visitors throughout different months using Disneyland Review Data which consists of 3 branches which are Disneyland Paris, Hong Kong and California. Sentiments and Ratings generally do not change much month to month. It is also found that Disneyland California has the highest ratings followed by Hong Kong and then Paris.")
    st.markdown("##### Bar Plots of Sentiments and Ratings")
    st.markdown("The sentiments and ratings do not vary drastically between different months. August has the lowest sentiment and rating among all the months. November has the highest rating and September has the best sentiment score.")
    st.pyplot(monthly_sentiment_scores(DisneylandReviews_data))
    st.pyplot(monthly_rating_scores(DisneylandReviews_data))

    #Line plot of ratings for all years and month for each park
    #st.pyplot(lineplot_ratings_all(DisneylandReviews_data))

    st.markdown("#### Heatmaps for Ratings")
    st.markdown("To further investigate, a heatmap is used to check rating differences for each branch. California and Hong Kong in general have higher ratings.")
    
    for fig in heatmap_ratings(DisneylandReviews_data):
        st.pyplot(fig)

    #st.markdown("### Heatmaps for Sentiments")
    #for fig in heatmap_sentiments(DisneylandReviews_data):
    #    st.pyplot(fig)

elif option == "Visitor Demographics":
    st.header("Visitor Demographics")
    st.markdown("In this section we investigate guest segments such as their Continent of Origin and Visit Type using Disneyland Review Data. We found that people from Europe and North America tend to give the most reviews. People visiting with their family give the most reviews out of all visit types. Months with more reviews also tend to be in line with Summer and Winter break. ")
    
    #Continent
    st.markdown("##### Continent of Origin Demographics")
    st.markdown("###### Continent and Month of Visit")
    st.markdown("People from North America and Europe tend to leave the most reviews consistently.")

    st.pyplot(continent_month_plot(DisneylandReviews_data))

    st.markdown("###### Continent of Origin and Rating/Sentiment Score")
    st.markdown("People from North America and Oceania tend to give higher ratings. Europeans give the lowest ratings")

    st.pyplot(continent_rating(DisneylandReviews_data))
    st.pyplot(continent_sentiment(DisneylandReviews_data))

    #Visit type
    st.markdown("#### Visit Type Demographics")
    st.markdown("Visitors were split into 5 types: Families, Couples, Friends, Solo and Unknown based on their reviews. Most people travel with their families")
    
    st.markdown("##### Visit Type and Month of Visit")
    st.markdown("Based on the reviews, most people travel with their family with June to August, October and December being the popular months. This is in line with school holidays such a Summer and Winter break. Guest going with their families tend to give the most reviews.")

    st.pyplot(visit_type_month(DisneylandReviews_data))

    st.markdown("##### Visit Type and Ratings/Sentiment Scores")
    st.markdown("Families tend to give poor ratings compared to other visit types although their sentiment score is not the lowest. It might be useful for theme park operators to investigate this discrepancy.")

    st.pyplot(visit_type_rating(DisneylandReviews_data))

    st.pyplot(visit_type_sentiment(DisneylandReviews_data))

elif option == "Ratings vs Attendance":
    st.markdown("### Ratings vs Attendance")
    st.markdown("Does higher ratings mean more attendance? We investigate this question using yearly Disneyland attendance data from the 3 branches and Disneyland Review data.  The correlation value of 0.525 suggests that there is a moderate positive relationship between previous year ratings and next year's attendance.")

    st.pyplot(correlation_plot(merged_df))