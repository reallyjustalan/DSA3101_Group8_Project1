# --- load_data.py ---
import pandas as pd
from pathlib import Path

def load_disney_data(filename="DisneylandReviews.csv", subfolder="B4"):
    """
    Load Disneyland review data from the data/ directory.

    Args:
        filename (str): Name of the CSV file to load.
        subfolder (str): Subfolder inside /data/ (default is 'B4').

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    base_dir = Path(__file__).resolve().parents[2]  # goes from scripts/B4 → scripts → project root
   # Navigate to project root from scripts/
    data_path = base_dir / "data" / subfolder / filename
    return pd.read_csv(data_path, encoding='ISO-8859-1')