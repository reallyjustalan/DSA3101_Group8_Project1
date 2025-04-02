import pandas as pd
import json

def clean_data(path):
    """
    Cleans the Disneyland reviews dataset.
    """
    # Load the dataset
    df = pd.read_csv(path, encoding='latin1')
    df['Branch'] = df['Branch'].astype('category')
    df["Year_Month"] = pd.to_datetime(df["Year_Month"], format="%Y-%m", errors = "coerce")
    df["Reviewer_Location"] = df["Reviewer_Location"].astype('category')
    df = df.rename(columns={
    "Reviewer_Location" : "Location"
    })
    return df

def random_sample(df, n=1000):
    """
    Returns a random sample of the dataframe.
    """
    return df.sample(n=n, random_state=1)


def load_json_to_dataframe(returned_responses, modelclass):
    all_reviews_data = []
    # If a single string is passed, convert to list
    if isinstance(returned_responses, str):
        returned_responses = [returned_responses]
    for returned_response in returned_responses:
        data = json.loads(returned_response)
        # Validate with Pydantic using model_validate (v2 method)
        if isinstance(data, list):
            validated_data = [modelclass.model_validate(item) for item in data]
        else:
            validated_data = [modelclass.model_validate(data)]
            
        for review in validated_data:
            for element in review.coded_elements:
                row = {
                    'review_id': review.review_id,
                    'touchpoint': element.touchpoint,
                    'sentiment': element.sentiment,
                    'code': element.code,
                    'text_excerpt': element.text_excerpt,
                    'travel_party': review.demographic_info.travel_party,
                    'first_visit': review.demographic_info.first_visit,
                    'visit_timing': review.demographic_info.visit_timing
                }
                all_reviews_data.append(row)
    
    # Create DataFrame from all collected data
    if all_reviews_data:
        df = pd.DataFrame(all_reviews_data)
        return df
    else:
        # Return empty DataFrame if no valid data
        return pd.DataFrame()