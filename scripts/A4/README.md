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

### `s01_datacollection_attendees.py`
Scrapes `queue-times.com` to collect attendee data for various theme parks and saves the results in `../data/raw/attendee.csv`.

- Uses `requests`, `BeautifulSoup`, and `pandas` for data extraction and processing.
- Retrieves historical attendee counts for theme parks.
- Uses helper functions from `s00_useful_functions.py`.
- Estimated runtime: ~4 minutes.

### `s02_datacollection_avg_crowd.py`
Scrapes `queue-times.com` to collect average crowd level data for various theme parks and saves the results in `../data/raw/avg_crowd.csv`.

- Uses `requests`, `BeautifulSoup`, and `pandas` for data extraction and processing.
- Extracts available years of data for each park.
- Collects monthly average crowd levels.
- Uses helper functions from `s00_useful_functions.py`.
- Estimated runtime: ~16 minutes.

### `s03_analysis_time_series.py`
This script focuses on preparing time series plots and performing STL decomposition for trend analysis of crowd levels over time. It includes functions for visualizing trends, seasonal patterns, and average crowd levels, as well as performing rolling mean calculations.

**Functions:**
* `plot_overall_avg_crowd_level`: Plots average crowd levels over time.
* `plot_overall_attendee_count`: Plots total attendee count over time.
* `plot_STL_decomposition`: Applies and plots seasonal decomposition of time series.
* `plot_centered_MA_3`: Plots a centered moving average (3-period) and highlights specific campaign periods.
* `get_trend`: Filters data and plots a 3-month moving average around a campaign date.
* `get_actual_data`: Plots actual data and highlights key campaign dates.

### s04_datacollection_kaggle.py
This script loads daily attendance data from a Kaggle dataset (from the user `ayushtankha/hackathon`) using the `kagglehub` library. It extracts the attendance data for the years 2012 to 2018, then saves it as a CSV file in the raw data folder.
* **Dependencies**: The script requires the `kagglehub` library, which can be installed with the command `pip install kagglehub[pandas-datasets]`.
* **Data Loading**: It uses `kagglehub.dataset_load` to fetch the dataset and load it into a pandas DataFrame.
* **Data Saving**: The data is saved into the `../data/raw/daily_attendance_2018_2022.csv` file.

### `s05_analysis_attendees.py`
* **Data Loading**: The script loads the daily attendance data (`daily_attendance_2018_2022.csv`) for a specific theme park, 'PortAventura World', between 2017 and 2020. The dataset is filtered to only include data for this theme park.
* **STL Decomposition**: * `get_STL_decomposition`: Uses the `STL` (Seasonal and Trend decomposition using LOESS) from the `statsmodels` library to decompose the attendance data into seasonal, trend, and residual components. The results are plotted and displayed.
* **Seasonal Decomposition**: * `get_seasonal_decomposition`: Decomposes the attendance data using a multiplicative seasonal model and plots the seasonal, trend, and residual components.
* **Visualization**: Both decomposition functions generate plots showing the decomposition of attendance data for the specified theme park.
* **Note on Plot Saving**: Some plot-saving code is currently commented out, but it can be enabled if needed.

#### 1. s06_analysis_avg_crowd.py
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

#### 2. s07_campaign_nlp.py
Purpose: NLP processing for theme park reviews and content.

#### 3. s08_kmeans_pca.py
Purpose: Campaign clustering and visualization.

#### 4. s09_google_scraping.py
Purpose: Disneyland review analysis.

#### 5. s10_retail_clean.py
Purpose: Retail data preprocessing.

#### 6. s11_retail_analysis.py
Purpose: RFM analysis implementation.

#### 7. s12_retail_modelling.py
Purpose: Customer segmentation modeling.

## Complete Workflows

### 1. Campaign Effectiveness Analysis
1. Load crowd data (`s06_analysis_avg_crowd.py`)
2. Calculate lift metrics for campaigns
3. Cluster campaigns (`s08_kmeans_pca.py`)
4. Visualize results

### 2. Customer Sentiment Analysis
1. Scrape/load reviews (`s09_google_scraping.py`)
2. Process text (`s07_campaign_nlp.py`)
3. Extract topics and sentiment

### 3. Customer Segmentation
1. Clean transaction data (`s10_retail_clean.py`)
2. Perform RFM analysis (`s11_retail_analysis.py`)
3. Build segmentation model (`s12_retail_modelling.py`)

## Installation & Setup

```bash
# Clone repository
git clone [repo-url]

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Install spaCy model
python -m spacy download en_core_web_sm