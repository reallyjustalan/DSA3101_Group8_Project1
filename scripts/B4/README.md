# B4

## How can we promptly address high-risk interactions to improve guest experience?

### `load_data.py`
  
This script provides a reusable function to load Disneyland review data from the `data/B4/` folder, regardless of where your script is being run from. To load your own dataset, ensure that your dataset is in the data/B4 folder and call load_disney_data(filename="your_dataset.csv", subfolder="B4"). 

---

**Features:**
- Uses `Path(__file__).resolve().parents[2]` to get the project root from inside `scripts/B4/` directory

---

**Used in:**
- `train_pipeline.py` to load the base Disneyland review dataset for labelling and model training

--- 

### `sentiment_labelling.py`
  
This script labels each review in the dataset with a 1 to 5 star rating using a pretrained BERT sentiment classifier from HuggingFace. The model used is `nlptown/bert-base-multilingual-uncased-sentiment`, which was fine-tuned for multilingual sentiment analysis on product reviews. The model predicts sentiment as a number of stars (from 1 to 5), which is aligned with the Rating scale used in the Disneyland review dataset. According to the model authors, this version reduces error by 40% on product reviews compared to older versions.

We chose this model over base BERT models or traditional rule-based approaches (e.g., VADER, TextBlob) for the following reasons:
1. **Fine-tuned on review-style data**  
Unlike generic BERT models, this model is optimized specifically to understand the tone and language of customer reviews, which often include mixed sentiments and sarcasm.

2. **Handles nuanced, varied-length text**  
Reviews are longer and more complex than short social media posts. Traditional sentiment tools like **VADER** and **TextBlob** performed poorly due to oversimplified sentiment rules and weak handling of negation and context.

---

The model is wrapped in a `transformers.pipeline()` for easy integration and the sentiment pipeline is applied to every row of the input DataFrame using `pandas.progress_apply()` with `tqdm` for progress tracking.

---

**Used in:**
- `train_pipeline.py` to generate sentiment labels on unlabelled reviews before filtering or training.

---
