# Scripts Folder Overview

This folder contains modular Python scripts for data preparation, feature engineering and modelling for predicting attraction demand.

---

## Script Sequence & Description

Please follow the order below when running the scripts:

1. **`Imports.py`**  
   All required package imports for the rest of the scripts.

2. **`P1.py`**  
   Predictor 1: Total Fatalities in Disney theme parks (by year).

3. **`main_dataset.py`**  
   Core structure of the main dataset, to be merged with other datasets later.

4. **`P2.py`**  
   Predictor 2: Weather data (Rainy vs. Non-Rainy days).

5. **`P3.py`**  
   Predictor 3: Natural disaster occurrences by type.

6. **`P4.py`**  
   Predictor 4: Number of public holidays in each month.

7. **`P5.py`**  
   Predictor 5: Seasonality (Spring, Summer, Fall, Winter).

8. **`P6.py`**  
   Predictor 6: Number of ongoing disasters by month.

9. **`P7.py`**  
   Predictor 7: Average number of night shows (Disney events) per month/year.

10. **`P8.py`**  
    Predictor 8: Market competition from nearby SeaWorld Orlando.

11. **`response_var.py`**  
    Engineering the response variable (attraction demand score).

12. **`modelling.py`**  
    Conducting model training and selection on candidate models using 5-fold cross-validation.

13. **`model_perf_plots.py`**  
    Visual comparison of model performance (MAE and RMSE).

14. **`feature_imp.py`**  
    Extracting feature importances and evaluating the final model.

---

## Note

Before running `main_dataset.py`, please extract the `waiting_times.csv` file into the `data/` folder.  
> GitHub prohibits uploading files >100 MB, so this file has been provided in compressed `.zip` format.

---

