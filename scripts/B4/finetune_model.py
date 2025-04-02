# --- finetune_model.py ---
import os
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from transformers import (
    AutoTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
)
from datasets import Dataset

# Disable Weights & Biases logging (remove this line to enable wandb logging)
os.environ["WANDB_DISABLED"] = "true"

def prepare_data(df_original=None, df_augmented=None, original_path=None, augmented_path=None):
    """
    Load and prepare training, validation, and test datasets from labelled and augmented reviews.
    Can accept either DataFrames directly or file paths.

    Args:
        df_original (pd.DataFrame, optional): Labelled original reviews.
        df_augmented (pd.DataFrame, optional): Augmented reviews.
        original_path (str, optional): CSV path to original reviews.
        augmented_path (str, optional): CSV path to augmented reviews.

    Returns:
        tuple: (train_ds, val_ds, test_ds, tokenizer)
    """
    if df_original is None:
        if original_path is None:
            raise ValueError("Either df_original or original_path must be provided.")
        df_original = pd.read_csv(original_path)

    if df_augmented is None:
        if augmented_path is None:
            raise ValueError("Either df_augmented or augmented_path must be provided.")
        df_augmented = pd.read_csv(augmented_path)

    df_original["risk_label"] = df_original["bert_sentiment"].apply(
        lambda x: 1 if x in ["1 star", "2 stars"] else 0
    )

    # First stratification safety check
    label_counts = df_original["risk_label"].value_counts()
    if any(label_counts < 2):
        raise ValueError("Not enough examples per class to stratify. Add more high-risk or low-risk data.")

    train_df, temp_df = train_test_split(
        df_original, test_size=0.3, stratify=df_original["risk_label"], random_state=42
    )

    # Second stratification safety check
    temp_label_counts = temp_df["risk_label"].value_counts()
    if any(temp_label_counts < 2):
        raise ValueError("Not enough examples per class in temp_df to stratify for validation/testing.")

    val_df, test_df = train_test_split(
        temp_df, test_size=0.5, stratify=temp_df["risk_label"], random_state=42
    )

    train_high_risk_original = train_df[train_df["risk_label"] == 1].copy()
    df_augmented_filtered = df_augmented[
        df_augmented["Review_Text"].isin(train_high_risk_original["Review_Text"])
    ].copy()
    df_augmented_filtered["risk_label"] = 1
    df_augmented_filtered = df_augmented_filtered.rename(columns={"back_translated_review": "Back_Translated_Text"})
    df_augmented_filtered = df_augmented_filtered.dropna(subset=["Back_Translated_Text"])
    df_augmented_filtered["Back_Translated_Text"] = df_augmented_filtered["Back_Translated_Text"].astype(str)

    train_df["Review_Text"] = train_df["Review_Text"].astype(str)
    val_df["Review_Text"] = val_df["Review_Text"].astype(str)
    test_df["Review_Text"] = test_df["Review_Text"].astype(str)

    original_train = train_df[["Review_Text", "risk_label"]].copy()
    augmented_train = df_augmented_filtered[["Back_Translated_Text", "risk_label"]].copy()
    augmented_train = augmented_train.rename(columns={"Back_Translated_Text": "Review_Text"})
    train_df_augmented = pd.concat([original_train, augmented_train], ignore_index=True)

    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    def tokenize(batch):
        return tokenizer(batch["text"], padding="max_length", truncation=True, max_length=256)

    train_ds = Dataset.from_pandas(
        train_df_augmented.rename(columns={"Review_Text": "text", "risk_label": "label"}).reset_index(drop=True)
    )
    val_ds = Dataset.from_pandas(
        val_df[["Review_Text", "risk_label"]].rename(columns={"Review_Text": "text", "risk_label": "label"}).reset_index(drop=True)
    )
    test_ds = Dataset.from_pandas(
        test_df[["Review_Text", "risk_label"]].rename(columns={"Review_Text": "text", "risk_label": "label"}).reset_index(drop=True)
    )

    train_ds = train_ds.map(tokenize, batched=True)
    val_ds = val_ds.map(tokenize, batched=True)
    test_ds = test_ds.map(tokenize, batched=True)

    return train_ds, val_ds, test_ds, tokenizer

def compute_metrics(eval_pred):
    """
    Compute evaluation metrics for classification.

    Args:
        eval_pred (tuple): (logits, labels) from Trainer.

    Returns:
        dict: Accuracy and F1 score.
    """
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1": f1_score(labels, preds)
    }

def finetune_model(train_ds, val_ds, tokenizer, save_dir=None):
    """
    Fine-tune a DistilBERT model on the given datasets and save it to data/B4.

    Args:
        train_ds (Dataset): Training dataset.
        val_ds (Dataset): Validation dataset.
        tokenizer: Tokenizer used for training.
        save_dir (str or Path): Directory to save the fine-tuned model.
    """
    if save_dir is None:
        save_dir = Path(__file__).resolve().parents[2] / "data" / "B4" / "distilbert_highrisk_model_final"
    save_dir.mkdir(parents=True, exist_ok=True)

    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

    training_args = TrainingArguments(
        output_dir="./bert-high-risk_output",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_dir="./logs",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=1,
        load_best_model_at_end=True,
        weight_decay=0.01,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )

    trainer.train()

    trainer.save_model(save_dir)
    tokenizer.save_pretrained(save_dir)
