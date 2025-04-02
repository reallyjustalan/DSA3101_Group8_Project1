# --- sentiment_labelling.py ---
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from tqdm import tqdm
import pandas as pd

def label_unlabelled_reviews(df, text_col="Review_Text", save_path=None):
    """
    Use a pretrained multilingual BERT sentiment model to label unlabelled reviews.

    Args:
        df (pd.DataFrame): DataFrame containing review text.
        text_col (str): Name of the column with text.
        save_path (str, optional): File path to save labelled results.

    Returns:
        pd.DataFrame: DataFrame with added 'bert_sentiment' column.
    """
    tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    tqdm.pandas()  # Enable progress bars with pandas
    df = df[[text_col]].dropna().copy()
    df["bert_sentiment"] = df[text_col].progress_apply(
        lambda x: sentiment_pipeline(x, truncation=True)[0]["label"]
    )

    if save_path:
        df.to_csv(save_path, index=False)

    return df