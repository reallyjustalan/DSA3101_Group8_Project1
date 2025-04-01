import kaggle
import pandas as pd
import numpy as np
import os
from pathlib import Path

# Set up directories and download data
downloads_path = str(Path.home() / "Downloads")
os.chdir(downloads_path)

# Authenticate and download dataset
try:
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files('ayushtankha/hackathon', path=downloads_path, unzip=True)
except Exception as e:
    print(f"Error downloading data: {e}")

# Load and process data
def load_and_process_data():
    # Read raw data
    attendance = pd.read_csv('attendance.csv')
    waiting_times = pd.read_csv('waiting_times.csv')
    link_attraction_park = pd.read_csv('link_attraction_park.csv')
    
    # Process waiting times to get attraction rankings
    ranking = waiting_times.groupby('ENTITY_DESCRIPTION_SHORT').agg({
        'GUEST_CARRIED': 'sum',
        'CAPACITY': 'mean'
    }).sort_values('GUEST_CARRIED', ascending=False)
    
    # Process attraction-park links
    link_attraction_park[['Attraction', 'Park']] = (
        link_attraction_park['ATTRACTION;PARK'].str.split(';', n=1, expand=True)
    )
    
    # Join rankings with park information
    attraction_ranking = ranking.join(
        link_attraction_park.set_index('Attraction'), 
        on='ENTITY_DESCRIPTION_SHORT'
    )
    
    return attraction_ranking

def create_park_rankings(attraction_ranking, park_name):
    """Create ranked attraction list for a specific park"""
    park_ranking = attraction_ranking[attraction_ranking['Park'] == park_name].copy()
    park_ranking['Ranking'] = range(1, len(park_ranking) + 1)
    return park_ranking

# Main processing
if __name__ == "__main__":
    attraction_ranking = load_and_process_data()
    
    # Create rankings for specific parks
    tivoli_ranking = create_park_rankings(attraction_ranking, 'Tivoli Gardens')
    
    # Save results
    tivoli_ranking.to_csv('tivoli_attr_ranking.csv', index=True)
    