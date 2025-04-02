## Overview

This sub-project contains Python scripts for historical and predictive crowd analysis. The analysis uses 2 data sets obtained from (https://www.kaggle.com/datasets/devinanzelmo/indoor-navigation-and-location-wifi-features):

1. `TrainingData.csv.csv`
2. `ValidationData.csv`

## Scripts

### 1. `LoadData.py`

This script loads the and combines the 2 data files from above. 'TrainingData.csv' consists of dates up to '2013-06-20' and 'ValidationData.csv' consists of dates from '2013-09-19'. The data has a gap of 3 months.

### 2. `Imports.py`

Contains all the imports we will use in this sub-project.

### 3. `vis_1_2.py`

Contains the code for data visualisation plots 1 and 2

### 4. `vis_3.py`

Contains the code for data visualisation plot 3

### 5. `vis_4.py`

Contains the code for data visualisation plot 4

### 6. `vis_5.py`

Contains the code for data visualisation plot 5

### 7. `vis_6.py`

Contains the code for data visualisation plot 6

### 8. `ml_1.py`

Contains code for data preprocessing for machine learning. Splits data back into training and test sets.

### 9. `train_n_save_models.py`

Contains code to train and save various regression models. Model is trained and validated on the training set.

### 10. `trained_models_1.py`

Contains code to load and test trained models on unseen data in the test set.

### 11. `custom_functions.py`

Contains various functions used throughout the sub-project.

### 12. `.joblib`

`.joblib` files contain their respective trained models.

## Instructions to run the script outside of streamlit

To run Visualisations outside of streamlit, simply select a vis_x.py file and run it.
To show model output, run `trained_models_1.py`. Do not run `train_n_save_models.py` unless creating new trained models.