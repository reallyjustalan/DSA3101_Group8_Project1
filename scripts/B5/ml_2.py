from custom_functions import evaluate_model
from models import models_1 as models
from ml_1 import *
from Imports import pd

# Train & Compare
results = []
for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train, y_train_reg_scaled)
    mse, r2, adj_r2 = evaluate_model(model, X_test_new, y_test_reg_new, coord_scaler, name) # X_val, y_val_reg can we swapped with X_test_new, y_test_reg_new
    results.append({
        'Model': name,
        'MSE': mse,
        'R²': r2,
        'Adjusted R²': adj_r2
    })

# Display results
results_df = pd.DataFrame(results).sort_values('MSE')
print("\n=== Model Comparison ===")
print(results_df.to_markdown(index=False))