from custom_functions import evaluate_model
#from models import models_1 as models
from ml_1 import *
from Imports import pd, os, plt

from Imports import (MultiOutputRegressor, XGBRegressor, GradientBoostingRegressor, 
                     RandomForestRegressor, SVR, MLPRegressor, dump)
from custom_functions import create_neural_network, adjusted_r2_score

models = {
    "XGBoost": MultiOutputRegressor(XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )),
    "Gradient Boosting": MultiOutputRegressor(GradientBoostingRegressor(
        n_estimators=150,
        max_depth=5,
        learning_rate=0.05,
        random_state=42
    )),
    "Random Forest": MultiOutputRegressor(RandomForestRegressor(
        n_estimators=200,
        max_depth=8,
        min_samples_split=5,
        random_state=42
    )),
    "SVR (RBF)": MultiOutputRegressor(SVR(
        kernel='rbf',
        C=1.0,
        epsilon=0.1
    )),
    "MLP": MLPRegressor(
        hidden_layer_sizes=(256, 128),
        activation='relu',
        solver='adam',
        early_stopping=True,
        random_state=42
    )
}

# Get the current script's directory
script_dir = os.path.dirname(__file__)

def display_results1():
    # Train & Compare
    results = []
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train_reg_scaled)

        # Save model to script directory
        model_filename = os.path.join(script_dir, f'{name.lower().replace(" ", "_")}_model.joblib')
        # dump(model, model_filename)
        print(f"Saved {name} model to {model_filename}")
        mse, r2, adj_r2, figures = evaluate_model(model, X_test_new, y_test_reg_new, coord_scaler, name) # X_val, y_val_reg can we swapped with X_test_new, y_test_reg_new
        for fig in figures:
            plt.figure(fig.number)
            plt.show()
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

display_results1()

