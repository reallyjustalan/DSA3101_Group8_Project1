from Imports import os, load
from ml_1 import *
import pandas as pd
from Imports import (MultiOutputRegressor, dump, GradientBoostingRegressor,
                    RandomForestRegressor, SVR, MLPRegressor, SVC, MLPClassifier, 
                    EarlyStopping, ReduceLROnPlateau, np, r2_score, mean_squared_error, 
                    plt, os, accuracy_score, classification_report, sns, confusion_matrix)
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

# print(loaded_models)

def evaluate_model_performance(model, X_test, y_test_reg, y_test_floors, coord_scaler, le, model_name):
    figures = []
    
   
    y_pred_reg = model['regressor'].predict(X_test)
    y_pred_reg = coord_scaler.inverse_transform(y_pred_reg)
    y_pred_floors = model['classifier'].predict(X_test)
    
    # Convert to numpy arrays if needed
    y_test_reg = np.array(y_test_reg) if not isinstance(y_test_reg, np.ndarray) else y_test_reg
    y_test_floors = np.array(y_test_floors)
    
    # Create formatted floor labels
    floor_labels = [f"Floor {int(i)}" for i in le.classes_]
    
    # Confusion Matrix
    fig1, ax1 = plt.subplots(figsize=(6, 5))
    cm = confusion_matrix(y_test_floors, y_pred_floors)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=floor_labels, 
                yticklabels=floor_labels, ax=ax1)
    ax1.set_title(f'{model_name} - Floor Confusion Matrix')
    ax1.set_xlabel('Predicted Floor')
    ax1.set_ylabel('Actual Floor')
    figures.append(fig1)
    
    # Coordinate Scatterplot
    fig2 = plt.figure(figsize=(6, 5))
    plt.scatter(y_test_reg[:, 0], y_test_reg[:, 1], alpha=0.5, label='Actual')
    plt.scatter(y_pred_reg[:, 0], y_pred_reg[:, 1], alpha=0.5, label='Predicted')
    plt.title(f'{model_name} - Coordinate Prediction')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    figures.append(fig2)
    
    # Residual Plots
    residuals = y_test_reg - y_pred_reg
    
    fig3, (ax2, ax3) = plt.subplots(1, 2, figsize=(12, 5))
    ax2.scatter(y_pred_reg[:, 0], residuals[:, 0], alpha=0.5)
    ax2.axhline(y=0, color='r', linestyle='--')
    ax2.set_title(f'{model_name} - Longitude Residuals')
    ax2.set_xlabel('Predicted Longitude')
    ax2.set_ylabel('Residuals')
    
    ax3.scatter(y_pred_reg[:, 1], residuals[:, 1], alpha=0.5)
    ax3.axhline(y=0, color='r', linestyle='--')
    ax3.set_title(f'{model_name} - Latitude Residuals')
    ax3.set_xlabel('Predicted Latitude')
    ax3.set_ylabel('Residuals')
    fig3.tight_layout()
    figures.append(fig3)
    
    # 3D Visualization
    fig4 = plt.figure(figsize=(8, 6))
    ax4 = fig4.add_subplot(111, projection='3d')
    ax4.scatter(y_test_reg[:, 0], y_test_reg[:, 1], y_test_floors, c='blue', marker='o', alpha=0.6, label='Actual')
    ax4.scatter(y_pred_reg[:, 0], y_pred_reg[:, 1], y_pred_floors, c='red', marker='x', alpha=0.6, label='Predicted')
    ax4.set_xlabel('Longitude')
    ax4.set_ylabel('Latitude')
    ax4.set_zlabel('Floor')
    ax4.set_title(f'{model_name} - 3D Position Comparison')
    ax4.legend()
    ax4.view_init(elev=25, azim=-60)
    figures.append(fig4)
    
    # Calculate metrics
    mse = mean_squared_error(y_test_reg, y_pred_reg)
    r2 = r2_score(y_test_reg, y_pred_reg)
    adj_r2 = adjusted_r2_score(y_test_reg, y_pred_reg, X_test.shape[1])
    accuracy = accuracy_score(y_test_floors, y_pred_floors)
    
    results_df = pd.DataFrame([{ 
        'Model': model_name,
        'MSE': mse,
        'R²': r2,
        'Adjusted R²': adj_r2,
        'Accuracy': accuracy
    }])
    
    return results_df, figures
for name, model in loaded_models.items():
    results_df, figures = evaluate_model_performance(model, X_test_new, y_test_reg_new, y_test_floors_new, coord_scaler, le, name)
    print(results_df)
