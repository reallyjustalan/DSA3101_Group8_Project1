from Imports import os, load
from models import evaluate_model_performance
from ml_1 import *
import pandas as pd
from Imports import (MultiOutputRegressor, GradientBoostingRegressor,
                    RandomForestRegressor, SVR, MLPRegressor, SVC, MLPClassifier, 
                    EarlyStopping, ReduceLROnPlateau, np, r2_score, mean_squared_error, 
                    plt, os, accuracy_score, classification_report, sns)
from custom_functions import create_neural_network, adjusted_r2_score

script_dir = os.path.dirname(__file__)
        
model_files = [
    'svr_(rbf)_regressor.joblib',
    'svr_(rbf)_classifier.joblib',
    'svr_(rbf)_metadata.joblib',
    'mlp_regressor.joblib',
    'mlp_classifier.joblib',
    'mlp_metadata.joblib'
]

# Dictionary to store loaded models
loaded_models = {}

# Load models
for filename in model_files:
    file_path = os.path.join(script_dir, filename)
    if os.path.exists(file_path):
        loaded_models[filename] = load(file_path)
        print(f"Loaded {filename} model from {file_path}")
    else:
        print(f"Warning: Could not find saved model for {filename}")

def evaluate_all_models_2(models, X_test, y_test_reg, y_test_floors, coord_scaler, le):
    results = []
    all_figures = {}
    
    for name, model in models.items():
        # Create figure
        fig = plt.figure(figsize=(20, 15))
        
        y_pred_reg = model['regressor'].predict(X_test)
        y_pred_reg = coord_scaler.inverse_transform(y_pred_reg)
        y_pred_floors = model['classifier'].predict(X_test)
        
        # Convert to numpy arrays
        y_test_reg = y_test_reg.values if hasattr(y_test_reg, 'values') else y_test_reg
        y_test_floors = np.array(y_test_floors)
        
        # Create plots (same as your evaluate_model_performance but returning figure)
        # ... [include all your plotting code from evaluate_model_performance] ...
        
        plt.tight_layout()
        
        # Calculate metrics
        mse = mean_squared_error(y_test_reg, y_pred_reg)
        r2 = r2_score(y_test_reg, y_pred_reg)
        accuracy = accuracy_score(y_test_floors, y_pred_floors)
        adj_r2 = adjusted_r2_score(y_test_reg, y_pred_reg, X_test.shape[1])
        
        results.append({
            'Model': name,
            'MSE': mse,
            'R²': r2,
            'Adj_R²': adj_r2,
            'Accuracy': accuracy
        })
        
        all_figures[name] = fig
    
    return pd.DataFrame(results).sort_values('MSE'), all_figures

evaluate_all_models_2(loaded_models, X_test, y_test_reg, y_test_floors, coord_scaler, le)