from Imports import (pd, np, MinMaxScaler, VarianceThreshold, r2_score, mean_squared_error, plt,
                     Dense, Input, Model)

def load_and_preprocess(df):
    """Load and preprocess raw dataframe"""
    df = df.sort_values(by=['TIMESTAMP'])
    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], unit='s')
    df['DATE'] = pd.to_datetime(df['TIMESTAMP'].dt.date)
    df['TIME'] = pd.to_datetime(df['TIMESTAMP'])
    # df = df.drop(columns=[col for col in df.columns if df[col].nunique() == 1] + ['RELATIVEPOSITION'])
    return df

def mean_exclude_100(arr):
    return arr[arr != 100].mean()

def preprocess_data(df, is_train=False, scaler=None, selector=None):
    """Apply all preprocessing steps consistently"""
    wap_cols = [col for col in df.columns if col.startswith("WAP")]
    
    # Signal processing
    df = df.replace(100, -120).fillna(-120)
    
    # Feature engineering
    #df['Strongest_Signal'] = df[wap_cols].max(axis=1)
    # df['Num_Strong_Signals'] = (df[wap_cols] > -30).sum(axis=1)
    df['Minute'] = pd.to_datetime(df['TIMESTAMP']).dt.minute
    #df['Signal_Variance'] = df[wap_cols].std(axis=1)  # Signal consistency
    #df['Signal_NonZero_Count'] = (df[wap_cols] > -90).sum(axis=1)  # Strong signal count
    #df['Signal_Range'] = df[wap_cols].max(axis=1) - df[wap_cols].min(axis=1)
    
    # Apply transformations
    df[wap_cols] = np.log10(df[wap_cols] + 121)
    df[wap_cols] = df[wap_cols].rolling(window=5, min_periods=1).mean()
    
    # Outlier handling
    Q1 = df[wap_cols].quantile(0.25)
    Q3 = df[wap_cols].quantile(0.75)
    IQR = Q3 - Q1
    df[wap_cols] = np.where(
        (df[wap_cols] < (Q1 - 1.5 * IQR)) | (df[wap_cols] > (Q3 + 1.5 * IQR)),
        np.nan,
        df[wap_cols]
    )
    df[wap_cols] = df[wap_cols].fillna(df[wap_cols].median())
    
    # Prepare features and targets
    X = df.drop(columns=['LONGITUDE', 'LATITUDE', 'FLOOR', 'BUILDINGID', 'SPACEID', 'TIMESTAMP', 'TIME', 'DATE'])
    y_reg = df[['LONGITUDE', 'LATITUDE']]
    y_cls = df['FLOOR']
    
    # Feature selection and scaling
    if is_train:
        scaler = MinMaxScaler(feature_range=(0, 1))
        
        selector = VarianceThreshold(threshold=0.01)
        
        X_scaled = scaler.fit_transform(X[wap_cols])
        X_scaled = selector.fit_transform(X_scaled)
        
        return X_scaled, y_reg, y_cls, scaler, selector, X.columns
    else:
        X_scaled = scaler.transform(X[wap_cols])
        X_scaled = selector.transform(X_scaled)
        return X_scaled, y_reg, y_cls
    
def adjusted_r2_score(y_true, y_pred, n_features):
    r2 = r2_score(y_true, y_pred)
    n_samples = len(y_true)
    return 1 - (1 - r2) * (n_samples - 1) / (n_samples - n_features - 1)

def evaluate_model(model, X_test, y_test, coord_scaler, model_name):
    # Ensure y_test is numpy array
    y_test = np.array(y_test) if not isinstance(y_test, np.ndarray) else y_test
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred = np.array(y_pred)  # Ensure numpy array
    y_pred = coord_scaler.inverse_transform(y_pred)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    adj_r2 = adjusted_r2_score(y_test, y_pred, X_test.shape[1])
    
    # Calculate residuals
    residuals = y_test - y_pred
    
    # Create plot figures
    figures = []
    
    # Figure 1: Residual plots
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.scatter(y_pred[:, 0], residuals[:, 0], alpha=0.5)
    ax1.axhline(y=0, color='r', linestyle='--')
    ax1.set_title(f'{model_name} - Longitude Residuals')
    ax1.set_xlabel('Predicted Longitude')
    ax1.set_ylabel('Residuals')
    
    ax2.scatter(y_pred[:, 1], residuals[:, 1], alpha=0.5)
    ax2.axhline(y=0, color='r', linestyle='--')
    ax2.set_title(f'{model_name} - Latitude Residuals') 
    ax2.set_xlabel('Predicted Latitude')
    ax2.set_ylabel('Residuals')
    fig1.tight_layout()
    figures.append(fig1)
    
    # Figure 2: Actual vs Predicted
    fig2 = plt.figure(figsize=(8, 6))
    plt.scatter(y_test[:, 0], y_test[:, 1], alpha=0.5, label='Actual')
    plt.scatter(y_pred[:, 0], y_pred[:, 1], alpha=0.5, label='Predicted')
    plt.title(f'{model_name} - Actual vs Predicted Coordinates')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    figures.append(fig2)
    
    return mse, r2, adj_r2, figures


def create_neural_network(input_shape, n_floors):
    inputs = Input(shape=(input_shape,))
    x = Dense(256, activation='relu')(inputs)
    x = Dense(128, activation='relu')(x)
    
    # Outputs
    coord_output = Dense(2, name='coord_output')(x)
    floor_output = Dense(n_floors, activation='softmax', name='floor_output')(x)
    
    model = Model(inputs=inputs, outputs=[coord_output, floor_output])
    model.compile(
        optimizer='adam',
        loss={
            'coord_output': 'mse',
            'floor_output': 'sparse_categorical_crossentropy'
        },
        metrics={
            'coord_output': ['mse'],
            'floor_output': ['accuracy']
        }
    )
    return model