from tqdm.auto import tqdm
import pandas as pd
import numpy as np
from google import genai
from google.genai import types

import configurations as c

# Load the data
df = pd.read_csv("../../data/A1/DisneylandReviews_Coded.csv")
print(df.iloc[1])
client = genai.Client(api_key=c.GEMINI)

def create_rich_embedding_text(row):
    return f"{row['code']}"

print("Creating rich text for embeddings...")
df['embedding_text'] = df.apply(create_rich_embedding_text, axis=1)
print(df['embedding_text'].head())

# Batch processing function
def process_in_batches(dataframe, batch_size=50):
    all_embeddings = []
    for i in tqdm(range(0, len(dataframe), batch_size), desc="Processing batches"):
        end_idx = min(i + batch_size, len(dataframe))
        batch = dataframe['embedding_text'].iloc[i:end_idx].tolist()
        try:
            result = client.models.embed_content(
                model="gemini-embedding-exp-03-07",
                contents=batch,
                config=types.EmbedContentConfig(task_type="CLUSTERING")
            )
            # Extract embeddings from response
            batch_embeddings = [emb.embedding for emb in result["embedding"]]
            print(result.embeddings)
            all_embeddings.extend(batch_embeddings)
        except Exception as e:
            print(f"Error in batch {i}-{end_idx}: {e}")
            # Fill failed batch with None values
            all_embeddings.extend([None] * len(batch))
            
    return all_embeddings

# Start batch embedding process
print("Starting batch embedding process...")
df["embedding"] = process_in_batches(df, batch_size=1)


output_path = "../../data/A1/DisneylandReviews_Embedded.csv"
print(f"Saving embeddings to {output_path}")
df.to_csv(output_path, index=False)

print(f"Total rows: {len(df)}")
print(f"Successful embeddings: {df['embedding'].notna().sum()}")
print(f"Failed embeddings: {df['embedding'].isna().sum()}")