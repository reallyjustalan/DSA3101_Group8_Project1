# --- main.py ---
from pathlib import Path
import pandas as pd
from topic_modelling import (
    run_classifier_on_test,
    create_custom_stopwords,
    run_topic_modelling
)

def main():
    base_dir = Path(__file__).resolve().parents[2]
    data_dir = base_dir / "data" / "B4"

    # Input: test dataset (use first 500 rows for testing)
    input_path = data_dir / "test_df.csv" # Replace with your dataset
    df = pd.read_csv(input_path)

    model_path = data_dir / "saved_distilbert_highrisk_model_final" # Replace with the path to your own weights if available

    # Run classifier and get predictions
    df["Review_Text"] = df["Review_Text"].astype(str)
    classified_df, high_risk_texts = run_classifier_on_test(df.copy(), model_path)

    # Save classifier-labelled output
    classified_output_path = data_dir / "classified_output.csv"
    classified_df.to_csv(classified_output_path, index=False)

    # Run topic modeling only if high-risk texts exist
    if high_risk_texts:
        clean_high_risk_texts = [str(t).strip() for t in high_risk_texts if isinstance(t, str) or pd.notna(t)]
        clean_high_risk_texts = [t for t in clean_high_risk_texts if len(t) > 0]

        stopwords = create_custom_stopwords()
        topic_model = run_topic_modelling(clean_high_risk_texts, stopwords)

        # Save topic modeling assignments
        topic_df = pd.DataFrame({
            "Review_Text": clean_high_risk_texts,
            "Topic": topic_model.get_document_info(clean_high_risk_texts)["Topic"]
        })
        topic_df.to_csv(data_dir / "topic_model_output.csv", index=False)

        # Save topic info
        topic_info = topic_model.get_topic_info()
        topic_info.to_csv(data_dir / "topic_info.csv", index=False)

        # topic_model.visualize_hierarchy(color_threshold=0.7) This can be saved as a file if needed
    else:
        print("⚠️  No high-risk reviews found — skipping topic modeling.")

    print("✅ Inference completed successfully.")

if __name__ == "__main__":
    main()