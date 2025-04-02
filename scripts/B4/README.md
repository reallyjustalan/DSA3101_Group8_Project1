# Flagging High-Risk Review 
Automatically classifies new review data and performs topic modelling on high-risk reviews. 

## Table of Contents
- [System Architecture](#system-architecture)
- [Dataset](#disneyland-reviews)
- [Inference Pipeline](#mainpy)
  - [Topic Modeling](#1-topic_modellingpy)
- [Training Pipeline (Optional)](#train_pipelinepy)
  - [load_data.py](#1-loaddatapy)
  - [sentiment_labelling.py](#2sentiment_labellingpy)
  - [data_augmentation.py](#3-data_augmentationpy)
  - [finetune_model.py](#4-fine-tune-a-classifier)
- [Running the Code](#running-the-code)


### System Architecture 
```text
       OPTIONAL: Training Workflow
       ───────────────────────────
      ┌───────────────────────────┐
      │     train_pipeline.py     │
      └─────────────┬─────────────┘
                    ▼
        ┌────────────────────────┐
        │     load_data.py       │
        ├────────────────────────┤
        │ sentiment_labelling.py │
        ├────────────────────────┤
        │ data_augmentation.py   │
        ├────────────────────────┤
        │   finetune_model.py    │
        └────────────┬───────────┘
                     ▼
     ┌────────────────────────────────────┐
     │  distilbert_highrisk_model_final/  │
     └────────────────────────────────────┘



        INFERENCE + TOPIC MODELING
        ──────────────────────────
              ┌─────────────┐
              │   main.py   │
              └──────┬──────┘
                     ▼
        ┌─────────────────────────┐
        │    topic_modelling.py   │
        └─────────────────────────┘
```

---

### Summary
- **Top block**: Training pipeline (optional — for retraining or updating the model)
- **Bottom block**: Inference pipeline using `main.py` and `topic_modelling.py` to classify and cluster new reviews

--- 

### Disneyland Reviews
The [dataset](https://www.kaggle.com/datasets/arushchillar/disneyland-reviews) contains 42,657 reviews from Disneyland California, Paris and Hong Kong. For this subquestion, only the Review_Text column is used. 

---

### `main.py`
This script runs the inference stage of the pipeline — applying a trained classifier to a new dataset and using BERTopic to extract topics from reviews classified as high-risk.

#### Output 
- The script creates two csv files called "topic_model_output.csv" and "topic_info.csv" in data/B4/ folder. 
- The former shows the high-risk reviews and their assigned topics, while the latter gives a summary of all discovered topics and keywords.

#### How to Use on Your Own Dataset?
`input_path = data_dir / "test_df.csv"`
- The value can be replaced by your dataset. Make sure to add your dataset to the data/B4/ folder before running and change the name of "test_df.csv" to your dataset.

`model_path = data_dir / "saved_distilbert_highrisk_model_final"`
- Fine-tuning the DistilBERT classifier can take a long time and hence, the model weights for the fine-tuned classifier on the Disneyland Reviews dataset is available in the data/B4 folder for use. However, if you want to use your own model configurations, simply change "saved_distilbert_highrisk_model_final" to your configuration folder. 

#### Note: Pretrained Model Weights
The `saved_distilbert_highrisk_model_final` folder (containing the fine-tuned binary classifier for high-risk review detection) is too large to store directly in this repository.  

**You can download the full model directory from Google Drive:**  
[Download `saved_distilbert_highrisk_model_final`](https://drive.google.com/drive/folders/1gNbQ2bJ4kQG3VoXAez6jgVmUPG0oAMaA?usp=sharing)

##### How to Use:
1. Open the Google Drive link above.
2. Download all **7 files** inside the folder:
   - `config.json`
   - `model.safetensors`
   - `special_tokens_map.json`
   - `tokenizer.json`
   - `tokenizer_config.json`
   - `training_args.bin`
   - `vocab.txt`
3. Create a folder named `saved_distilbert_highrisk_model_final` inside your `data/B4/` directory.
4. Move all the downloaded files into that folder.

Your directory structure should look like:

```
data/
└── B4/
    └── saved_distilbert_highrisk_model_final/
        ├── config.json
        ├── model.safetensors
        ├── special_tokens_map.json
        ├── tokenizer.json
        ├── tokenizer_config.json
        ├── training_args.bin
        └── vocab.txt
```

This folder will be automatically used by `main.py`.


## `train_pipeline.py`
This script runs the complete training pipeline for the binary risk classifier. It sequentially performs sentiment labelling, data augmentation, dataset preparation, and model fine-tuning using DistilBERT.

#### How to Use on Your Own Dataset?
`labelled_path = data_dir / "Labelled_DisneylandReviews_test.csv"`
- To use your own dataset instead, make sure the dataset is added to the data/B4/ folder and change the name of the csv file "Labelled_DisneylandReviews_test.csv" to your dataset.
`augmented_path = data_dir / "Labelled_DisneylandReviews_Augmented_test.csv"`
- For clarity, the name of the augmented file should also be changed. 


## Scripts in `main.py`

### 1. `topic_modelling.py`
This script performs topic modeling on predicted high-risk reviews using the [BERTopic](https://maartengr.github.io/BERTopic/) framework. It first classifies the test data using the fine-tuned DistilBERT model and then extracts coherent topics from the subset of reviews identified as high-risk.


## Scripts in `train_pipeline.py`

### 1. `load_data.py`
  
This script provides a reusable function to load Disneyland review data from the `data/B4/` folder, regardless of where your script is being run from. 

The file uses `Path(__file__).resolve().parents[2]` to get the project root from inside `scripts/B4/` directory.

**Used in:**
- `train_pipeline.py` to load the base Disneyland review dataset for labelling and model training

--- 

### 2.`sentiment_labelling.py`
  
This script labels each review in the dataset with a 1 to 5 star rating using a pretrained BERT sentiment classifier from HuggingFace. The model used is `nlptown/bert-base-multilingual-uncased-sentiment`, which was fine-tuned for multilingual sentiment analysis on product reviews. The model predicts sentiment as a number of stars (from 1 to 5), which is aligned with the Rating scale used in the Disneyland review dataset. According to the model authors, this version reduces error by 40% on product reviews compared to older versions.

We chose this model over base BERT models or traditional rule-based approaches (e.g., VADER, TextBlob) for the following reasons:
- **Fine-tuned on review-style data**  
Unlike generic BERT models, this model is optimized specifically to understand the tone and language of customer reviews, which often include mixed sentiments and sarcasm.

- **Handles nuanced, varied-length text**  
Reviews are longer and more complex than short social media posts. Traditional sentiment tools like VADER and TextBlob performed poorly due to oversimplified sentiment rules and weak handling of negation and context.

The model is wrapped in a `transformers.pipeline()` for easy integration and the sentiment pipeline is applied to every row of the input DataFrame using `pandas.progress_apply()` with `tqdm` for progress tracking.

**Output**
- This script creates a csv file named "Labelled_DisneylandReviews.csv" in the data/B4/ folder.

**Used in:**
- `train_pipeline.py` to generate sentiment labels on unlabelled reviews before filtering or training.

---

### 3. `data_augmentation.py`

To address class imbalance in our binary classification task, we performed data augmentation via back-translation on the minority class - defined as **high-risk reviews** (those labeled as `1 star` or `2 stars`). The `augment_high_risk_reviews()` function in `data_augmentation.py` applies back-translation to all high-risk reviews using the `deep-translator` library, and saves the new dataset with a `back_translated_review` column.

#### Why is it a Classification Task?

The sentiment model labels the reviews according to star ratings from 1 to 5. However, we reframed this problem as a binary classification task, instead of a regression task, as the business question seeks to identify which reviews represent high-risk guest experiences that require attention.

Hence, we grouped the sentiment labels as follows:
- `1 star` or `2 stars` → **High Risk** → Label: `1`
- `3 stars`, `4 stars`, `5 stars` → **Not High Risk** → Label: `0`

#### Class Distribution

After applying sentiment labelling, the class distribution was highly imbalanced for the minority class:

| Sentiment  | Count | Percentage |
|------------|-------|------------|
| 1 star     | 2386  | 5.59%      |
| 2 stars    | 5093  | 11.94%     |
| 3 stars    | 4767  | 11.18%     |
| 4 stars    | 14428 | 33.82%     |
| 5 stars    | 15982 | 37.47%     |

High-risk reviews (`1 star` and `2 stars`) account for **only ~17.5%** of the dataset. The rest are non-high-risk.

Therefore, to prevent the classifier from becoming biased toward the dominant class (non-high-risk), we needed more training examples from the high-risk class. We applied data augmentation using back-translation to synthetically generate new training samples.

#### Why Back-Translation?
We chose back-translation over other augmentation techniques as it preservers semantics while changing phrasing, produces varied sentence structures naturally and avoids overfitting to repeated phrases which usually occurs with simple duplication.

While SMOTE (Synthetic Minority Oversampling Technique) is a popular choice for synthetic data generation, it is designed for numerical tabular data and not text. Applying SMOTE to vector embeddings create unnatural sentences which do not accurately reflect the real data. Likewise, Paraphrasing models often produce repetitive or low-diversity outputs, and may not generalize well across review styles.

**Output** 
- This script saves a csv file named "Labelled_DisneylandReviews_Augmented.csv" in the data/B4/ folder

**Used in:**
- `train_pipeline.py` to generate additional high-risk training examples by back-translating reviews labeled as `1 star` or `2 stars`.

---

### 4. `finetune_model.py`
This script handles the full fine-tuning pipeline for a DistilBERT model used to classify reviews as either high-risk or non-high-risk.

The input dataset is split using 70/15/15 for train, test and evaluation set and stratified splitting is used to maintain the class ratio (high-risk vs non-high-risk) in all sets. Augmented reviews (from `data_augmentation.py`) are filtered to include only those that match high-risk examples in the training set. These are then appended to the original training set to increase representation of the minority class (high-risk reviews).

#### Why DistilBERT?

To identify high-risk reviews, we chose to fine-tune the distilbert-base-uncased model from Hugging Face. DistilBERT is a distilled version of BERT that is 40% smaller, 60% faster, and yet retains 97% of BERT’s language understanding capabilities. This makes it an ideal tradeoff between performance and efficiency, especially for deployment in resource limited environments.

We picked DistilBERT over traditional models that rely on bag-of-words or TF-IDF representations (eg Logistic Regression, SVM, Naive Bayes) as these struggle with long and nuanced reviews.

**Output**
- This script saves a fine-tuned DistilBERT model and tokenizer for binary classification in the data/B4/distilbert_highrisk_model_final/ folder

**Used in:**
- `train_pipeline.py` as the final step after labelling and augmenting the data.


---

### Running the Code

To train your own model (optional):
```bash
cd scripts
python B4/train_pipeline.py
```
To classify and extract topics from new reviews:

```bash
cd scripts
python B4/main.py
```
Make sure your data is saved in the `data/B4/` folder before running either script.

