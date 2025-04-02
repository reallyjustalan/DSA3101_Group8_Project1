# --- train_pipeline.py ---
from pathlib import Path
from load_data import load_disney_data
from sentiment_labelling import label_unlabelled_reviews
from data_augmentation import augment_high_risk_reviews
from finetune_model import prepare_data, finetune_model

def main():
    """
    Full training pipeline to label, augment, and fine-tune a DistilBERT classifier.
    All generated files are saved in the data/B4 directory.
    """
    # Set paths
    base_dir = Path(__file__).resolve().parents[2]
    data_dir = base_dir / "data" / "B4"

    labelled_path = data_dir / "Labelled_DisneylandReviews_test.csv"
    augmented_path = data_dir / "Labelled_DisneylandReviews_Augmented_test.csv"

    # Load raw data
    df = load_disney_data().head(10) 

    # Generate sentiment labels and save
    labelled_df = label_unlabelled_reviews(df, save_path=labelled_path)

    # Augment high-risk reviews and save
    augmented_df = augment_high_risk_reviews(labelled_df, save_path=augmented_path)

    # Prepare training, validation, and test sets (no need to save these for now)
    train_ds, val_ds, test_ds, tokenizer = prepare_data(
        df_original=labelled_df,
        df_augmented=augmented_df
    )

    # Fine-tune model and save to default save_dir
    finetune_model(train_ds, val_ds, tokenizer)

if __name__ == "__main__":
    main()
