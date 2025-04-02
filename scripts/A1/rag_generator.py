from tqdm.auto import tqdm
import pandas as pd
import numpy as np
from google import genai
import configurations as c
import time
import random
from google.genai import types  

# Load the data
df = pd.read_csv("../../data/A1/DisneylandReviews_Coded.csv")

# Initialize Google API client
client = genai.Client(api_key=c.GEMINI)

# Function to create rich text for embedding
def create_rich_embedding_text(row):
    return f"{row['touchpoint']} - {row['code']}: {row['text_excerpt']})"

# Apply function to create embedding text
print("Creating rich text for embeddings...")
df['embedding_text'] = df.apply(create_rich_embedding_text, axis=1)

# Batch processing function with exponential backoff
def process_in_batches(dataframe, batch_size=10, initial_delay=5):
    all_embeddings = []
    current_delay = initial_delay
    max_delay = 60  # Maximum delay of 60 seconds
    
    # Process in batches with much smaller batch size
    for i in tqdm(range(0, len(dataframe), batch_size), desc="Processing batches"):
        end_idx = min(i + batch_size, len(dataframe))
        batch = dataframe['embedding_text'].iloc[i:end_idx].tolist()
        
        success = False
        retry_count = 0
        max_retries = 5
        
        while not success and retry_count < max_retries:
            try:
                # Add jitter to avoid synchronized retries
                actual_delay = current_delay + random.uniform(0, 1)
                print(f"Waiting {actual_delay:.2f} seconds before batch {i}-{end_idx}...")
                time.sleep(actual_delay)
                
                # Updated to include the task_type parameter for CLUSTERING
                result = client.models.embed_content(
                    model="gemini-embedding-exp-03-07",
                    contents=batch,
                    config={"task_type": "CLUSTERING", 
                            "output_dimensionality" : 500}
                )
                
                # Extract the values
                batch_embeddings = [emb.values for emb in result.embeddings]
                all_embeddings.extend(batch_embeddings)
                
                # Success! Reduce the delay slightly (but keep it reasonable)
                current_delay = max(initial_delay, current_delay * 0.9)
                success = True
                
            except Exception as e:
                retry_count += 1
                print(f"Error in batch {i}-{end_idx} (attempt {retry_count}/{max_retries}): {e}")
                
                # Exponential backoff with jitter
                current_delay = min(max_delay, current_delay * 2)
                
                if retry_count >= max_retries:
                    print(f"Max retries reached for batch {i}-{end_idx}. Skipping.")
                    # Fill with None values for failed batch
                    all_embeddings.extend([None] * len(batch))
        
        # Save progress after each batch
        if i % (batch_size * 5) == 0 and i > 0:
            temp_df = dataframe.copy()
            temp_df["embedding"] = all_embeddings + [None] * (len(temp_df) - len(all_embeddings))
            temp_df.to_csv(f"../../data/A1/DisneylandReviews_Embedded_progress_{i}.csv", index=False)
            print(f"Progress saved at batch {i}")
            
    return all_embeddings

# Start batch embedding process with very conservative parameters
print("Starting batch embedding process...")
df["embedding"] = process_in_batches(df, batch_size=5, initial_delay=2)

# Save the dataframe with embeddings
output_path = "../../data/A1/DisneylandReviews_Embedded.csv"
print(f"Saving embeddings to {output_path}")
df.to_csv(output_path, index=False)

# Print statistics
print(f"Total rows: {len(df)}")
print(f"Successful embeddings: {df['embedding'].notna().sum()}")
print(f"Failed embeddings: {df['embedding'].isna().sum()}")