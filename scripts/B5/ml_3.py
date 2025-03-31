from models import evaluate_model_performance
from ml_1 import *
from Imports import pd
from models import models_2 as models



results = []
for name, model in models.items():
    print(f"\n{'='*40}\nEvaluating {name}\n{'='*40}")
    
    if name != "Neural Network":
        model['regressor'].fit(X_train, y_train_reg_scaled)
        model['classifier'].fit(X_train, y_train_floors)
    
    metrics = evaluate_model_performance(
        model, X_test_new, y_test_reg_new, y_test_cls_new, # X_val, y_val_reg, y_val_floors can we swapped with X_test_new, y_test_reg_new, y_test_cls_new
        coord_scaler, le, name
    )
    results.append({'Model': name, **metrics})

# Display final comparison
results_df = pd.DataFrame(results).sort_values('MSE')
print("\n=== Final Model Comparison ===")
print(results_df.to_markdown(index=False))