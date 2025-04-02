# Documentation for A5 Seasonality Demographics

This document aims to explain the code for subquestion A5 which seeks to investigate how does seasonality, public holidays and visitor demographics impact theme park attendance and reviews.

The scripts and the functions are explained below.


## Data Cleaning Scripts

The datasets used are:
    1. attendance.csv which shows monthly attendance data of PortAventura and Tivoli Gardens from 2018 to 2022 
    2. DisneylandReviews.csv which shows reviews from Disneyland Hong Kong, Paris and California from 2010 to 2019
    3. Yearly Attendance Disney Paris Hong Kong Cali.xlsx which shows yearly attendance for Disneyland Hong Kong,
    Paris and California.

The data has been sourced from https://www.kaggle.com/datasets/ayushtankha/hackathon/data?select=waiting_times.csv,
https://www.kaggle.com/datasets/arushchillar/disneyland-reviews/data and from https://queue-times.com/parks
respectively.

### Data_Cleaning_AttendanceA5.py

This script consists of 1 function to clean attendance.csv which is saved as cleaned_attendance.csv

Steps performed:
    1. Removes duplicate rows
    2. Converts the 'USAGE_DATE' column to datetime format
    3. Extracts 'Year', 'Month', and 'Day_of_Week' from 'USAGE_DATE'
    4. Ensures no negative values exist in the 'attendance' column and converts to 0 
    5. Computes mean and standard deviation of attendance per facility and year.
    6. Standardizes attendance values.

### Data_Cleaning_DisneylandReviewsA5.py

This script consists of 1 function to clean DisneylandReviews.csv which is saved as cleaned_DisneylandReviews.csv

Steps performed:
    1. Removes rows with missing values in the 'Year_Month' column.
    2. Converts 'Year_Month' to datetime format and extracts 'Year' and 'Month'.
    3. Applies VADER sentiment analysis for each review.
    4. Categorizes reviews by visit type (e.g., Family, Couples, Friends, Solo) based on keywords in reviews.
    5. Find continent of the reviewer based on country of origin.

### Data_Cleaning_AttendanceDisneyA5.py

This script consists of 1 function to clean Yearly Attendance Disney Paris Hong Kong Cali.xlsx which is saved as cleaned_disney_attendance.csv

Steps performed:
    1. Strips spaces and converts the 'Attendance' column to numeric.
    2. Group the smaller parks into the main parks
    3. Groups data by 'Year' and 'Park' summing attendance values.


## EDA Scripts

The scripts will use the cleaned csv files for Exploratory Data Analysis (EDA) to help answer how does seasonality,
public holidays and visitor demographics impact theme park attendance and reviews.


### Disneyland_Sentiment_RatingsA5.py

This script analyzes Disneyland reviews to explore trends in ratings and sentiment scores. Various visualization
techniques, such as bar plots, line plots, and heatmaps, are used to gain insights into the data.
cleaned_DisneylandReviews.csv is used in this script.

#### 1. monthly_sentiment_scores(DisneylandReviews_data)

    -Computes and visualizes average sentiment scores per month.
    -Displays a bar plot showing sentiment variations by month.
    -Sentiments are mostly constant throughout the months, with the highest in November (0.706328) and the lowest in August (0.652312).

#### 2. monthly_rating_scores(DisneylandReviews_data)

    -Computes and visualizes average ratings per month.
    -Displays a bar plot showing rating variations by month.
    -Ratings remain mostly constant, with the highest in September (4.362229) and the lowest in August (4.115423).

#### 3. lineplot_ratings_all(DisneylandReviews_data)

    -Creates a line plot of average ratings per month for each year and branch.
    -Uses a facet grid to plot separate plots for each Disneyland location.

#### 4. heatmap_ratings(DisneylandReviews_data)

    -Generates heatmaps showing rating variations across different years and months for each branch.
    -Disneyland California has the highest ratings, followed by Hong Kong, then Paris.

#### 5. heatmap_month_branch_ratings(DisneylandReviews_data)

    -Generates heatmaps displaying average monthly ratings for each Disneyland branch.
    -Allows for a comparative analysis of how ratings change across locations over time.

#### 6. heatmap_sentiments(DisneylandReviews_data)

    -Creates heatmaps illustrating sentiment score variations across different years and months for each branch.

### Disneyland_Visit_ContinentsA5.py

This script analyzes and visualizes cleaned_DisneylandReviews.csv. It explores visitor demographics, sentiment
analysis, and rating trends using seaborn and matplotlib visualizations.

#### 1. continent_month_plot(DisneylandReviews_data)

    -Generates a heatmap showing the number of reviews per continent per month.
    -North America and Europe consistently leave the most reviews.

#### 2. visit_type_month(DisneylandReviews_data)

    -Creates a line plot showing trends in visit types over different months.
    -Families travel mostly during summer and winter breaks.

#### 3. visit_type_rating(DisneylandReviews_data)

    -Generates a bar plot of average ratings by visit type.
    -Solo travelers tend to give better ratings, while families rate experiences lower.

#### 4. visit_type_sentiment(DisneylandReviews_data)

    -Creates a bar plot showing the average sentiment score by visit type.

#### 5. continent_rating(DisneylandReviews_data)

    -Creates a bar plot of average ratings by continent.
    -People from North America and Oceania give better ratings while people from Europe give poorer ratings.

#### 6. continent_sentiment(DisneylandReviews_data)

    -Generates a bar plot showing the average sentiment score by continent.

### Local_Holidays_Plots_TivoliPortAventuraA5.py

This script analyzes cleaned_attendance.csv to check for differences in attendance between holidays and non-holidays as well as between different holidays for Port Avenutura in Spain and Tivoli Gardens in Denmark.

#### 1. port_aventura_holidays_stat_test(attendance_data)

    -Performs a statistical t-test comparing park attendance on holidays vs. non-holidays for PortAventura World.
    -The difference in attendance for holidays and non-holidays is statistically significant.

#### 2. port_aventura_holidays_plot(attendance_data)

    -Creates a bar plot showing average attendance on specific holidays at PortAventura World.
    -Christmas and New Year's see the most attendance among the other holidays.

#### 3. tivoli_holidays_stat_test(attendance_data)

    -Performs a statistical t-test comparing park attendance on holidays vs. non-holidays for Tivoli Gardens.
    -The difference in attendance for holidays and non-holidays is statistically significant.

#### 4. tivoli_holidays_plot(attendance_data)

    -Creates a bar plot showing average attendance on specific holidays at Tivoli Gardens.
    -Christmas, Boxing Day and New Year's see the most attendance among the other holidays.

### Ratings_vs_AttendanceA5.py

This script uses cleaned_disney_attendance.csv and cleaned_DisneylandReviews.csv to investigate if there is a relationship between past ratings and future attendance.

#### 1. merged_disney(attendance_disney, DisneylandReviews_data)

    -Merge attendance and review data, shifting ratings by one year to check if previous year ratings affects attendance in the nest function.

#### 2. correlation_plot(merged_df)

    -Plots correlation plot of current year attendance against previous year ratings.
    -The correlation value of 0.525 suggests that there is a moderate positive relationship between previous year ratings and next year's attendance.

### Time_Series_Plots_TivoliPortAventuraA5.py

This script uses cleaned_attendance.csv to investigate the time series trends for Port Aventura and Tivoli Gardens.

#### 1. tivoli_PortAventura_overview(attendance_data)

    -Generate a line plot showing attendance trends over time for PortAventura and Tivoli.
    -The Covid-19 pandemic which started in March 2020 and ended in May 2023 affected data within those years as shown in the dip in 2020 and saw 0 attendance for some periods in 2020 and 2021. It also took some time for attendance to increase to pre-pandemic levels.

#### 2. tivoli_PortAventura_all_time(attendance_data)

    -Generate line plots showing monthly attendance trends for each year.

#### 3. tivoli_PortAventura_weekly_trend_max(attendance_data)

    -Generate a bar plot showing which days had the most count of maximum attendance per month.
    -Saturday has the most count of maximum attendance per month.

#### 4. tivoli_PortAventura_weekly_trend_mean(attendance_data)

    -Generate a bar plot showing the mean attendance for each day of the week.
    -Saturday has the most mean attendance.

## Requirements
holidays==0.68
matplotlib==3.10.1
nltk==3.9.1
numpy==2.2.4
pandas==2.2.3
pycountry_convert==0.7.2
scipy==1.15.2
seaborn==0.13.2
streamlit==1.44.0
