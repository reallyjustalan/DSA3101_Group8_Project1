# --- topic_modelling.py ---
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from pathlib import Path

def run_classifier_on_test(test_df, model_path):
    """
    Run a pre-trained classifier on the test set to get predicted labels.

    Args:
        test_df (pd.DataFrame): Test set with review text.
        model_path (str or Path): Path to the saved model directory.

    Returns:
        tuple: (DataFrame with predicted labels, list of high-risk texts)
    """
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, return_all_scores=False)

    test_texts = test_df["Review_Text"].astype(str).tolist()
    predictions = classifier(test_texts, batch_size=8, truncation=True)

    test_df = test_df.copy()
    test_df["predicted_label"] = [1 if p["label"] == "LABEL_1" else 0 for p in predictions]
    high_risk_texts = test_df[test_df["predicted_label"] == 1]["Review_Text"].dropna().astype(str).tolist()

    return test_df, high_risk_texts

def create_custom_stopwords():
    """
    Create a custom stopword list for BERTopic vectorization.

    Returns:
        set: Set of extended stopwords.
    """
    stopwords = set(ENGLISH_STOP_WORDS)
    stopwords.update([ # List of stopwords can be edited to suit your dataset
        "disneyland", "disney", "park", "hong", "kong", "hk",
        "visit", "visiting", "went", "ride", "rides", "day", "just",
        "got", "go", "line", "time", "like", "also", "one", "even" 
    ])
    return stopwords

def run_topic_modelling(texts, stopwords):
    """
    Run BERTopic on a list of high-risk review texts.

    Args:
        texts (list): List of strings (review texts).
        stopwords (set): Set of stopwords to exclude from topic modeling.

    Returns:
        BERTopic: Trained BERTopic model.
    """
    vectorizer_model = CountVectorizer(stop_words=list(stopwords))
    topic_model = BERTopic(vectorizer_model=vectorizer_model)
    topics, probs = topic_model.fit_transform(texts)
    return topic_model
