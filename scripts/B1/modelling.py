from response_var import df
from Imports import *
# Train-Test split

# Features and target variable
X = df.drop(columns=["Demand_Score"])  # Features
y = df["Demand_Score"]  # Target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Verifying split sizes
print(f"Training data size: {X_train.shape[0]} samples")
print(f"Test data size: {X_test.shape[0]} samples")

# Linear Regression
lr_model = LinearRegression()

# Cross-validation for RMSE 
rmse_scores_lr = cross_val_score(lr_model, X_train, y_train, cv=5, scoring="neg_mean_squared_error")
average_rmse_lr = np.mean(np.sqrt(np.abs(rmse_scores_lr)))

# Cross-validation for MAE
mae_scores_lr = cross_val_score(lr_model, X_train, y_train, cv=5, scoring="neg_mean_absolute_error")
average_mae_lr = np.mean(np.abs(mae_scores_lr))  

# Standardizing features for Ridge, Lasso, and Elastic Net

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Scaling features in training data only
X_test_scaled = scaler.transform(X_test)  # Transforming test data (for possible later evaluation)

# Ridge Regression (Finding optimal alpha using training data)
ridge_params = {'alpha': np.logspace(-1, 3, 50)}
ridge_grid = GridSearchCV(Ridge(), ridge_params, scoring="neg_mean_squared_error", cv=5)
ridge_grid.fit(X_train_scaled, y_train)

optimal_alpha_ridge = ridge_grid.best_params_['alpha']  # Best alpha value

# Train Ridge model with optimal alpha
ridge_model = Ridge(alpha=optimal_alpha_ridge)

# Cross-validation for RMSE
rmse_scores_ridge = cross_val_score(ridge_model, X_train_scaled, y_train, cv=5, scoring="neg_mean_squared_error")
average_rmse_ridge = np.mean(np.sqrt(np.abs(rmse_scores_ridge)))  

# Cross-validation for MAE
mae_scores_ridge = cross_val_score(ridge_model, X_train_scaled, y_train, cv=5, scoring="neg_mean_absolute_error")
average_mae_ridge = np.mean(np.abs(mae_scores_ridge)) 

# Lasso Regression (Finding optimal alpha using training data)
lasso_params = {'alpha': np.logspace(-3, 3, 50)}  
lasso_grid = GridSearchCV(Lasso(max_iter=10000), lasso_params, scoring="neg_mean_squared_error", cv=5)
lasso_grid.fit(X_train_scaled, y_train)

optimal_alpha_lasso = lasso_grid.best_params_['alpha']  # Best alpha value

# Train Lasso model with optimal alpha
lasso_model = Lasso(alpha=optimal_alpha_lasso, max_iter=10000)

# Cross-validation for RMSE
rmse_scores_lasso = cross_val_score(lasso_model, X_train_scaled, y_train, cv=5, scoring="neg_mean_squared_error")
average_rmse_lasso = np.mean(np.sqrt(np.abs(rmse_scores_lasso)))  

# Cross-validation for MAE
mae_scores_lasso = cross_val_score(lasso_model, X_train_scaled, y_train, cv=5, scoring="neg_mean_absolute_error")
average_mae_lasso = np.mean(np.abs(mae_scores_lasso))

# Elastic Net Regression (Finding optimal alpha and l1_ratio using training data)
elastic_params = {
    'alpha': np.logspace(-3, 3, 30),  
    'l1_ratio': np.linspace(0.1, 0.9, 9) 
}
elastic_grid = GridSearchCV(ElasticNet(max_iter=10000), elastic_params, scoring="neg_mean_squared_error", cv=5)
elastic_grid.fit(X_train_scaled, y_train)

optimal_alpha_elastic = elastic_grid.best_params_['alpha']
optimal_l1_ratio = elastic_grid.best_params_['l1_ratio']

# Train Elastic Net model with optimal alpha and l1_ratio
elastic_model = ElasticNet(alpha=optimal_alpha_elastic, l1_ratio=optimal_l1_ratio, max_iter=10000)

# Cross-validation for RMSE
rmse_scores_elastic = cross_val_score(elastic_model, X_train_scaled, y_train, cv=5, scoring="neg_mean_squared_error")
average_rmse_elastic = np.mean(np.sqrt(np.abs(rmse_scores_elastic)))  

# Cross-validation for MAE
mae_scores_elastic = cross_val_score(elastic_model, X_train_scaled, y_train, cv=5, scoring="neg_mean_absolute_error")
average_mae_elastic = np.mean(np.abs(mae_scores_elastic))  

# Single Decision Tree

dt_model = DecisionTreeRegressor(random_state=42)

# Defining hyperparameter grid
param_grid = {
    'max_depth': [3, 5, 10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# RMSE Tuning
rmse_scorer = make_scorer(mean_squared_error, greater_is_better=False, squared=False)

grid_rmse = GridSearchCV(
    estimator=dt_model,
    param_grid=param_grid,
    scoring=rmse_scorer,
    cv=5,
    n_jobs=-1
)

grid_rmse.fit(X_train, y_train)  

# MAE Tuning
mae_scorer = make_scorer(mean_absolute_error, greater_is_better=False)

grid_mae = GridSearchCV(
    estimator=dt_model,
    param_grid=param_grid,
    scoring=mae_scorer,
    cv=5,
    n_jobs=-1
)

grid_mae.fit(X_train, y_train)

# Tuned Decision Tree (RMSE)
optimal_params_dt_rmse = grid_rmse.best_params_
average_rmse_dt_tuned = -grid_rmse.best_score_

# Tuned Decision Tree (MAE)
optimal_params_dt_mae = grid_mae.best_params_
average_mae_dt_tuned = -grid_mae.best_score_

# Random Forest

rf_model = RandomForestRegressor(random_state=42)

# Defining hyperparameter grid
param_grid_rf = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}

# RMSE Tuning
rmse_scorer = make_scorer(mean_squared_error, greater_is_better=False, squared=False)

grid_rf_rmse = GridSearchCV(
    estimator=rf_model,
    param_grid=param_grid_rf,
    scoring=rmse_scorer,
    cv=5,
    n_jobs=-1
)

grid_rf_rmse.fit(X_train, y_train)

# MAE Tuning
mae_scorer = make_scorer(mean_absolute_error, greater_is_better=False)

grid_rf_mae = GridSearchCV(
    estimator=rf_model,
    param_grid=param_grid_rf,
    scoring=mae_scorer,
    cv=5,
    n_jobs=-1
)

grid_rf_mae.fit(X_train, y_train)

# Tuned Random Forest (RMSE)
optimal_params_rf_rmse = grid_rf_rmse.best_params_
average_rmse_rf_tuned = -grid_rf_rmse.best_score_

# Tuned Random Forest (MAE)
optimal_params_rf_mae = grid_rf_mae.best_params_
average_mae_rf_tuned = -grid_rf_mae.best_score_

# Overall results (Average CV RMSE and MAE)

print(f"Average CV RMSE for Multiple Linear Regression: {average_rmse_lr:.4f}")
print(f"Average CV MAE for Multiple Linear Regression: {average_mae_lr:.4f}")
print(f"Optimal Ridge Penalty: {optimal_alpha_ridge:.4f}")
print(f"Average CV RMSE for Ridge Regression: {average_rmse_ridge:.4f}")
print(f"Average CV MAE for Ridge Regression: {average_mae_ridge:.4f}")
print(f"Optimal Lasso Penalty: {optimal_alpha_lasso:.4f}")
print(f"Average CV RMSE for Lasso Regression: {average_rmse_lasso:.4f}")
print(f"Average CV MAE for Lasso Regression: {average_mae_lasso:.4f}")
print(f"Optimal Elastic Net Alpha: {optimal_alpha_elastic:.4f}, L1 Ratio: {optimal_l1_ratio:.2f}")
print(f"Average CV RMSE for Elastic Net Regression: {average_rmse_elastic:.4f}")
print(f"Average CV MAE for Elastic Net Regression: {average_mae_elastic:.4f}")
print(f"Optimal Parameters for Decision Tree (RMSE): {optimal_params_dt_rmse}")
print(f"Average CV RMSE for Tuned Decision Tree: {average_rmse_dt_tuned:.4f}")
print(f"Optimal Parameters for Decision Tree (MAE): {optimal_params_dt_mae}")
print(f"Average CV MAE for Tuned Decision Tree: {average_mae_dt_tuned:.4f}")
print(f"Optimal Parameters for Random Forest (RMSE): {optimal_params_rf_rmse}")
print(f"Average CV RMSE for Tuned Random Forest: {average_rmse_rf_tuned:.4f}")
print(f"Optimal Parameters for Random Forest (MAE): {optimal_params_rf_mae}")
print(f"Average CV MAE for Tuned Random Forest: {average_mae_rf_tuned:.4f}")

