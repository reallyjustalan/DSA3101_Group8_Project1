from Imports import *
from modelling import *

# Feature Importance for Random Forest model

# Using the optimally tuned Random Forest model (RMSE-based)
best_rf_model = grid_rf_rmse.best_estimator_
best_rf_model.fit(X_train, y_train)
feature_importance = best_rf_model.feature_importances_
feature_importance_df = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': feature_importance
}).sort_values(by="Importance", ascending=False)
print(feature_importance_df)

# Evaluating Test RMSE and MAE for Tuned Random Forest Model
y_pred_rf = best_rf_model.predict(X_test)
# Test RMSE
rmse_test_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
# Test MAE
mae_test_rf = mean_absolute_error(y_test, y_pred_rf)

print(f"Test RMSE for Tuned Random Forest: {rmse_test_rf:.4f}")
print(f"Test MAE for Tuned Random Forest: {mae_test_rf:.4f}")