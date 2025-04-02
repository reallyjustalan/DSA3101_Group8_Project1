from Imports import os, load, pd
from custom_functions import evaluate_model
from ml_1 import *

results = []
loaded_models = {}
script_dir = os.path.dirname(__file__)

models = [
    "XGBoost", "Gradient Boosting", "Random Forest", "SVR (RBF)", "MLP"]

# 1. First load all saved models
for name in models:
    filename = os.path.join(script_dir, f'{name.lower().replace(" ", "_")}_model.joblib')
    if os.path.exists(filename):
        loaded_models[name] = load(filename)
        print(f"Loaded pre-trained {name} model from {filename}")
    else:
        print(f"Warning: Could not find saved model for {name}")
        # Optionally train if not found
        # loaded_models[name] = models[name]
        # loaded_models[name].fit(X_train, y_train_reg_scaled)

# commented out code is to test to see if models are able to load in correctly.
"""
# 2. Evaluate all loaded models
for name, model in loaded_models.items():
    print(f"\nEvaluating {name}...")
    mse, r2, adj_r2 = evaluate_model(model, X_test_new, y_test_reg_new, coord_scaler, name)
    results.append({
        'Model': name,
        'MSE': mse,
        'R²': r2,
        'Adjusted R²': adj_r2
    })

# Display results
results_df = pd.DataFrame(results).sort_values('MSE')
print("\n=== Model Comparison ===")
print(results_df.to_markdown(index=False))"""

def evaluate_all_models(loaded_models, X_test_new, y_test_reg_new, coord_scaler):
    results = []
    all_figures = {}
    
    for name, model in loaded_models.items():
        print(f"\nEvaluating {name}...")
        mse, r2, adj_r2, figures = evaluate_model(model, X_test_new, y_test_reg_new, coord_scaler, name)
        
        results.append({
            'Model': name,
            'MSE': mse,
            'R²': r2,
            'Adjusted R²': adj_r2
        })
        all_figures[name] = figures
    
    results_df = pd.DataFrame(results).sort_values('MSE')
    return results_df, all_figures