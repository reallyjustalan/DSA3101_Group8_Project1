import apigenerator
import dfhelper
import pandas as pd


# df = dfhelper.clean_data("../../data/A1/DisneylandReviews.csv")
# df = dfhelper.random_sample(df, n=1000)
# df.to_csv("../../data/A1/DisneylandReviews_Sample.csv", index=False)
df = pd.read_csv("../../data/A1/DisneylandReviews_Sample.csv")
final_list = apigenerator.process_inputs(
    [f"ID: {row['Review_ID']}, Review Text: {row['Review_Text']}, Where the reviewer is from: {row['Location']}, Disney Branch: {row['Branch']}" 
     for _, row in df.iterrows()], 
    delay=0)
rendered_df = dfhelper.load_json_to_dataframe(final_list, apigenerator.ReviewAnalysis)
rendered_df.to_csv("../../data/A1/DisneylandReviews_Coded.csv", index=False)
