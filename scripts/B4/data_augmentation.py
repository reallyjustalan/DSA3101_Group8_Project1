# --- data_augmentation.py ---
from deep_translator import GoogleTranslator
from tqdm import tqdm
import pandas as pd

def back_translate(text, intermediate_lang="fr"):
    """
    Perform back-translation for data augmentation.

    Args:
        text (str): Original text in English.
        intermediate_lang (str): Language to translate to and back (default is French).

    Returns:
        str: Back-translated text.
    """
    try:
        translated = GoogleTranslator(source='auto', target=intermediate_lang).translate(text) # English to intermediate
        back_translated = GoogleTranslator(source=intermediate_lang, target='en').translate(translated) # Back to English
        return back_translated
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def augment_high_risk_reviews(df, text_col="Review_Text", sentiment_col="bert_sentiment", save_path=None):
    """
    Apply back-translation to high-risk reviews (1-star or 2-star).

    Args:
        df (pd.DataFrame): DataFrame with labelled reviews.
        text_col (str): Column containing the review text.
        sentiment_col (str): Column with sentiment labels.
        save_path (str, optional): Path to save augmented CSV.

    Returns:
        pd.DataFrame: DataFrame with an added column 'back_translated_review'.
    """
    high_risk_df = df[df[sentiment_col].isin(["1 star", "2 stars"])].dropna(subset=[text_col]).copy()

    tqdm.pandas() # Progress bar
    high_risk_df["back_translated_review"] = high_risk_df[text_col].progress_apply(back_translate)

    if save_path:
        high_risk_df.to_csv(save_path, index=False)

    return high_risk_df
