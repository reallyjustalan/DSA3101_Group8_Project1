from Imports import (MultiOutputRegressor, XGBRegressor, GradientBoostingRegressor, 
                     RandomForestRegressor, SVR, MLPRegressor, SVC, MLPClassifier, EarlyStopping, ReduceLROnPlateau, np,
                     r2_score, mean_squared_error, plt, confusion_matrix, accuracy_score, classification_report, sns)
from custom_functions import create_neural_network, adjusted_r2_score
from ml_1 import *

# Defining various models to compare performance.
models_1 = {
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

# NN_Wrapper class to store predictions
class NN_Wrapper:
    def __init__(self, model, coord_scaler):
        self.model = model
        self.coord_scaler = coord_scaler
        
    def predict_all(self, X):
        """Returns both regression and classification predictions"""
        pred_reg, pred_cls = self.model.predict(X, verbose=0)
        return self.coord_scaler.inverse_transform(pred_reg), np.argmax(pred_cls, axis=1)
    
# Create the neural network model
nn_model = create_neural_network(X_train.shape[1], len(le.classes_))

# Train the nn_model
history = nn_model.fit(
    X_train,
    {'coord_output': y_train_reg_scaled, 'floor_output': y_train_floors},
    validation_data=(X_val, {'coord_output': coord_scaler.transform(y_val_reg), 'floor_output': y_val_floors}),
    epochs=100,
    callbacks = [
        EarlyStopping(patience=10, restore_best_weights=True),
        ReduceLROnPlateau(factor=0.5, patience=5)],
    batch_size=64,
    verbose=1
)
    
models_2 = {
    "SVR (RBF)": {
        'regressor': MultiOutputRegressor(SVR(kernel='rbf')),  # SVR for regression
        'classifier': SVC(kernel='rbf')                       # SVC for classification
    },
    "MLP": {
        'regressor': MLPRegressor(hidden_layer_sizes=(256, 128), early_stopping=True),
        'classifier': MLPClassifier(hidden_layer_sizes=(256, 128), early_stopping=True)
    },
    "Neural Network": NN_Wrapper(nn_model, coord_scaler)  
}

# Function to evaluate model performance
def evaluate_model_performance(model, X_test, y_test_reg, y_test_floors, coord_scaler, le, model_name):
   
    plt.figure(figsize=(20, 15))
    
    # Make predictions
    if isinstance(model, NN_Wrapper):  # Neural Network case
        y_pred_reg, y_pred_floors = model.predict_all(X_test)
    else:  # Traditional ML case
        y_pred_reg = model['regressor'].predict(X_test)
        y_pred_reg = coord_scaler.inverse_transform(y_pred_reg)
        y_pred_floors = model['classifier'].predict(X_test)
    
    # Convert to numpy arrays if needed
    y_test_reg = y_test_reg.values if hasattr(y_test_reg, 'values') else y_test_reg
    y_test_floors = np.array(y_test_floors)
    
    # Create formatted floor labels
    floor_labels = [f"Floor {int(i)}" for i in le.classes_]
    
    # Confusion Matrix
    plt.subplot(2, 3, 1)
    cm = confusion_matrix(y_test_floors, y_pred_floors)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
               xticklabels=floor_labels, 
               yticklabels=floor_labels)
    plt.title(f'{model_name} - Floor Confusion Matrix')
    plt.xlabel('Predicted Floor')
    plt.ylabel('Actual Floor')
    
    # Coordinate Scatterplot
    plt.subplot(2, 3, 2)
    plt.scatter(y_test_reg[:, 0], y_test_reg[:, 1], alpha=0.5, label='Actual')
    plt.scatter(y_pred_reg[:, 0], y_pred_reg[:, 1], alpha=0.5, label='Predicted')
    plt.title('Coordinate Prediction')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    
    # Residual Plots
    residuals = y_test_reg - y_pred_reg
    
    plt.subplot(2, 3, 4)
    plt.scatter(y_pred_reg[:, 0], residuals[:, 0], alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.title('Longitude Residuals')
    plt.xlabel('Predicted Longitude')
    plt.ylabel('Residuals')
    
    plt.subplot(2, 3, 5)
    plt.scatter(y_pred_reg[:, 1], residuals[:, 1], alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.title('Latitude Residuals')
    plt.xlabel('Predicted Latitude')
    plt.ylabel('Residuals')
    
    # 4. 3D Visualization
    ax = plt.subplot(2, 3, (3,6), projection='3d')
    ax.scatter(y_test_reg[:, 0], y_test_reg[:, 1], y_test_floors,
              c='blue', marker='o', alpha=0.6, label='Actual')
    ax.scatter(y_pred_reg[:, 0], y_pred_reg[:, 1], y_pred_floors,
              c='red', marker='x', alpha=0.6, label='Predicted')
    """
    # Add error lines
    for i in range(len(y_test_reg)):
        ax.plot([y_test_reg[i,0], y_pred_reg[i,0]],
                [y_test_reg[i,1], y_pred_reg[i,1]],
                [y_test_floors[i], y_pred_floors[i]],
                'gray', alpha=0.2, linestyle='--')"""
    
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Floor')
    ax.set_title('3D Position Comparison')
    ax.legend()
    ax.view_init(elev=25, azim=-60)
    
    plt.tight_layout()
    plt.show()
    
    # Calculate metrics
    mse = mean_squared_error(y_test_reg, y_pred_reg)
    r2 = r2_score(y_test_reg, y_pred_reg)
    accuracy = accuracy_score(y_test_floors, y_pred_floors)
    adj_r2 = adjusted_r2_score(y_test_reg, y_pred_reg, X_test.shape[1])

    
    print(f"\n=== {model_name} Performance ===")
    print(f"Coordinates MSE: {mse:.4f}")
    print(f"Coordinates R²: {r2:.4f}")
    print(f"Floor Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test_floors, y_pred_floors, target_names=floor_labels))
    
    return {
        'MSE': mse,
        'R²': r2,
        'Adj_R²': adj_r2,
        'Accuracy': accuracy
    }