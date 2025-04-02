from LoadData import df
from custom_functions import preprocess_data
from Imports import train_test_split, StandardScaler, LabelEncoder

# Prepare training and test data
df_00 = df[df['BUILDINGID'] == 0] # Change this number [0, 1, 2] for different buildings. ===============================================
df_0 = df_00[df_00['DATE'] < '2013-07-20']
df_0_test = df_00[df_00['DATE'] > '2013-07-20']

# Process training data
X_train, y_train_reg, y_train_cls, scaler, selector, train_cols = preprocess_data(df_0, is_train=True)

# Process test data
X_test_new, y_test_reg_new, y_test_cls_new = preprocess_data(df_0_test, is_train=False, scaler=scaler, selector=selector)

# Split training data for validation
X_train, X_val, y_train_reg, y_val_reg, y_train_cls, y_val_cls = train_test_split(
    X_train, y_train_reg, y_train_cls, test_size=0.2, random_state=42
)

# Scale regression targets
coord_scaler = StandardScaler()
y_train_reg_scaled = coord_scaler.fit_transform(y_train_reg)
y_val_reg_scaled = coord_scaler.transform(y_val_reg)

# Encode categorical element
le = LabelEncoder()
y_train_floors = le.fit_transform(y_train_cls)  
y_val_floors = le.transform(y_val_cls)     