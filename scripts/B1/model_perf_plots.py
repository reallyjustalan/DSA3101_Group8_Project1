from modelling import *

models = [
    "Linear Regression", "Ridge Regression", "Lasso Regression", "Elastic Net Regression",
    "Decision Tree Regression", "Random Forest Regression"
]
# RMSE values
rmse_values = [
    average_rmse_lr, average_rmse_ridge, average_rmse_lasso, average_rmse_elastic,
    average_rmse_dt_tuned, average_rmse_rf_tuned
]

# MAE values
mae_values = [
    average_mae_lr, average_mae_ridge, average_mae_lasso, average_mae_elastic,
    average_mae_dt_tuned, average_mae_rf_tuned
]

# Plot RMSE
plt.figure(figsize=(10, 5))
plt.bar(models, rmse_values, color='blue')
plt.xlabel("Models")
plt.ylabel("Average RMSE")
plt.title("Average CV RMSE for Different Models")
plt.xticks(rotation=45, ha="right")
plt.show()

# Plot MAE
plt.figure(figsize=(10, 5))
plt.bar(models, mae_values, color='green')
plt.xlabel("Models")
plt.ylabel("Average MAE")
plt.title("Average CV MAE for Different Models")
plt.xticks(rotation=45, ha="right")
plt.show()