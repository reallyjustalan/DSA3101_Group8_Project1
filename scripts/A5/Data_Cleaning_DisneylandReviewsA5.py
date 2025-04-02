import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pycountry_convert as pc

def disneylandReviews_data_cleaning(file_location):
    """
    Cleans and processes Disneyland reviews data 
    
    Steps performed:
    1. Removes rows with missing values in the 'Year_Month' column.
    2. Converts 'Year_Month' to datetime format and extracts 'Year' and 'Month'.
    3. Applies VADER sentiment analysis for each review.
    4. Categorizes reviews by visit type (e.g., Family, Couples, Friends, Solo) based on keywords in reviews.
    5. Find continent of the reviewer based on country of origin.
    
    """
    DisneylandReviews_data = pd.read_csv(file_location, encoding="latin-1")
    
    DisneylandReviews_data = DisneylandReviews_data.dropna(subset=["Year_Month"])  # Remove rows with missing dates

    #Convert to datetime
    DisneylandReviews_data["Year_Month"] = pd.to_datetime(
        DisneylandReviews_data["Year_Month"], format="%Y-%m", errors="coerce"
    )

    #Make a separate year and month column
    DisneylandReviews_data["Year"] = DisneylandReviews_data["Year_Month"].dt.year
    DisneylandReviews_data["Month"] = DisneylandReviews_data["Year_Month"].dt.month

    # Apply VADER sentiment analysis to the reviews
    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()
    DisneylandReviews_data["Sentiment_Score"] = DisneylandReviews_data["Review_Text"].apply(lambda x: sia.polarity_scores(str(x))["compound"])

    #Find visit type based on key words found in review text
    DisneylandReviews_data['Visit_Type'] = DisneylandReviews_data['Review_Text'].apply(lambda x: 
        'Family' if any(word in x.lower() for word in ['family', 'my kids', 'the kids', 'my children', 'parents', 'wife', 'husband', 'baby', 
                        'toddler', 'son', 'daughter', 'mom', 'dad', 'grandma', 'grandpa', 'grandmother', 'grandfather', 'grandchild', 'grandchildren', 'grandson', 'grandaughter', 
                        'cousins', 'nephew', 'niece', 'the kids', 'little ones', 'family-friendly']) else
        'Couples' if any(word in x.lower() for word in ['boyfriend', 'girlfriend', 'my partner', 'honeymoon', 'fiance', 'fiancee', 'anniversary trip', 'couples retreat' ]) else                                                                                 
        'Friends' if any(word in x.lower() for word in ['friends', 'buddies', 'hangout', 'bestie', 'friend']) else                                                                
        'Solo' if any(word in x.lower() for word in ['solo trip', 'by myself']) else 'Unknown'
    )

    #Continent to see which continent the reviewers are from
    def country_to_continent(country_name):
        try:
            country_alpha2 = pc.country_name_to_country_alpha2(country_name)
            country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
            country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
            return country_continent_name
        except:
            return "Unknown"  # Handle errors (e.g., missing or incorrect country names)

    # Apply function to the 'Reviewer_Location' column
    DisneylandReviews_data["Continent"] = DisneylandReviews_data["Reviewer_Location"].apply(country_to_continent)

    return DisneylandReviews_data


if __name__ == "__main__":
    disneylandReviews_data_cleaning("data/A5/DisneylandReviews.csv")