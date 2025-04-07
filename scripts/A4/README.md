# Overview
This sub-project contains Pythons scripts for subquestion A4, which seeks to analyze the impact of market strategies on guest behaviour.

## Scripts
# Project Name

## Overview
This project contains a collection of scripts designed for data processing, analysis, and optimization in theme park staffing and guest experience modeling. The repository is structured for modular use, with reusable functions, data processing scripts, and analysis modules.

## Scripts Overview

### `s00_useful_functions.py`
A collection of reusable utility functions used across multiple scripts.

- `get_indices()`: Reads and returns a list of park indices from `accepted_indices.txt`.
- `check_invalid_page(soup)`: Checks whether a webpage contains valid data.

### `s00A_get_indices.py`
Scrapes `queue-times.com` to retrieve valid theme park indices and saves them to `../data/raw/accepted_indices.txt`.

- Uses `requests` and `BeautifulSoup` for web scraping.
- Iterates through possible indices and checks for valid pages.
- Saves accepted park indices in a text file.
- Estimated runtime: ~4.5 minutes.


### `s01_datacollection_avg_crowd.py`
Scrapes `queue-times.com` to collect average crowd level data for various theme parks and saves the results in `../data/raw/avg_crowd.csv`.

- Uses `requests`, `BeautifulSoup`, and `pandas` for data extraction and processing.
- Extracts available years of data for each park.
- Collects monthly average crowd levels.
- Uses helper functions from `s00_useful_functions.py`.
- Estimated runtime: ~16 minutes.

#### `s02_analysis_avg_crowd.py`
Purpose: Measures campaign effectiveness through crowd level analysis.

Key Features:
- Calculates absolute and percentage lift for theme park campaigns
- Handles both pre-COVID and post-COVID data periods
- Compares campaign months against seasonal averages
- Returns detailed campaign performance metrics

Key Functions:
- get_attraction_campaign_df(): Filters data for specific campaigns
- get_lift_of_campaign(): Calculates campaign lift metrics

Dependencies:
- pandas
- datetime

#### `s04_retail_clean.py`
Purpose: clean missing values

1A - Description NA values (0.27% of total observations) DROP
1B - CustomerID NA values (~25% of total observations) DROP
1C - Cancellation orders (1.71% of total observations) DROP
1D - Quantity negative values (~0% of total observations) DROP
1  - TOTAL 26.58% dropped

Dependencies:
- pandas

#### `s05_retail_analysis.py`
Purpose: clean data analysis and preprocessesing for KMeans modelling
Since k-means is a distance based algorithm, we have to ensure that all 
numerical variable are scaled.

Dependencies:
- numpy
- pandas
- plotly
- scipy
- sklearn

#### `s06_retail_modelling.py`
Purpose: Customer segmentation modeling. Find best K for KMeans

Dependencies:
- pandas
- plotly
- scipy
- sklearn
- yellowbrick

## Complete Workflows
1. Obtain raw data (`s01_datacollection_avg_crowd.py`)

### 1. Campaign Effectiveness Analysis
1. Calculate marketing lift (`s02_analysis_avg_crowd`)
1. Load marketing effectiveness model (`s03_marketing_clustering.py`)
2. Visualize results

### 3. Customer Segmentation
1. Clean transaction data (`s04_retail_clean.py`)
2. Perform RFM analysis (`s05_retail_analysis.py`)
3. Build segmentation model (`s06_retail_modelling.py`)
4. Visualize results

## Installation & Setup

```bash
# Clone repository
git clone [repo-url]

# Install dependencies
pip install -r requirements.txt
