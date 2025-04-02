from models import evaluate_model_performance
from ml_1 import *
import pandas as pd
from Imports import (MultiOutputRegressor, dump, GradientBoostingRegressor,
                    RandomForestRegressor, SVR, MLPRegressor, SVC, MLPClassifier, 
                    EarlyStopping, ReduceLROnPlateau, np, r2_score, mean_squared_error, 
                    plt, os, accuracy_score, classification_report, sns)
from custom_functions import create_neural_network, adjusted_r2_score

class NN_Wrapper:
    def __init__(self, model, coord_scaler):
        self.model = model
        self.coord_scaler = coord_scaler
        
    def predict_all(self, X):
        """Returns both regression and classification predictions"""
        pred_reg, pred_cls = self.model.predict(X, verbose=0)
        return self.coord_scaler.inverse_transform(pred_reg), np.argmax(pred_cls, axis=1)

def initialize_models(X_train, y_train_reg_scaled, y_train_floors, coord_scaler, le):
    """Initialize and train all models"""
    # Create neural network
    nn_model = create_neural_network(X_train.shape[1], len(le.classes_))
    history = nn_model.fit(
        X_train,
        {'coord_output': y_train_reg_scaled, 'floor_output': y_train_floors},
        validation_data=(X_val, {'coord_output': coord_scaler.transform(y_val_reg), 'floor_output': y_val_floors}),
        epochs=100,
        callbacks=[
            EarlyStopping(patience=10, restore_best_weights=True),
            ReduceLROnPlateau(factor=0.5, patience=5)],
        batch_size=64,
        verbose=1
    )

    models = {
        "SVR (RBF)": {
            'regressor': MultiOutputRegressor(SVR(kernel='rbf')),
            'classifier': SVC(kernel='rbf')
        },
        "MLP": {
            'regressor': MLPRegressor(hidden_layer_sizes=(256, 128), early_stopping=True),
            'classifier': MLPClassifier(hidden_layer_sizes=(256, 128), early_stopping=True)
        },
        "Neural Network": NN_Wrapper(nn_model, coord_scaler)  
    }

    # Train non-NN models
    for name, model in models.items():
        if name != "Neural Network":
            model['regressor'].fit(X_train, y_train_reg_scaled)
            model['classifier'].fit(X_train, y_train_floors)
    
    return models

script_dir = os.path.dirname(__file__)

def save_hybrid_models(models, coord_scaler, le, script_dir):
    """Save all hybrid models to disk"""
    saved_files = []
    
    for name, model in models.items():
        if isinstance(model, NN_Wrapper):
            # Special handling for neural network
            model_filename = os.path.join(script_dir, f'{name.lower().replace(" ", "_")}_model')

            # Save the Keras model
            model.model.save(f'{model_filename}_nn.h5')

            # Save the wrapper metadata
            dump({
                'coord_scaler': coord_scaler,
                'model_type': 'neural_network'
            }, f'{model_filename}_wrapper.joblib')

            print(f"Saved {name} model to {model_filename}_nn.h5 and {model_filename}_wrapper.joblib")
            saved_files.append(f'{model_filename}_nn.h5')
            saved_files.append(f'{model_filename}_wrapper.joblib')
            
        else:
            # Save traditional ML models
            model_filename = os.path.join(script_dir, f'{name.lower().replace(" ", "_")}')
            
            # Save regressor and classifier separately
            dump(model['regressor'], f'{model_filename}_regressor.joblib')
            dump(model['classifier'], f'{model_filename}_classifier.joblib')
            
            # Save metadata
            dump({
                'coord_scaler': coord_scaler,
                'label_encoder': le,
                'model_type': 'traditional'
            }, f'{model_filename}_metadata.joblib')
            
            print(f"Saved {name} components to {model_filename}_[regressor|classifier|metadata].joblib")
            saved_files.extend([
                f'{model_filename}_regressor.joblib',
                f'{model_filename}_classifier.joblib'
            ])
    
    return saved_files

models = initialize_models(X_train, y_train_reg_scaled, y_train_floors, coord_scaler, le)

# Save models
saved_files = save_hybrid_models(models, coord_scaler, le, script_dir)
print(f"\nSaved all model files: {saved_files}")