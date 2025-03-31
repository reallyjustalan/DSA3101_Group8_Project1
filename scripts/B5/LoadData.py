from Imports import pd

# 1. Load and preprocess data
def load_and_preprocess(df):
    """Load and preprocess raw dataframe"""
    df = df.sort_values(by=['TIMESTAMP'])
    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], unit='s')
    df['DATE'] = pd.to_datetime(df['TIMESTAMP'].dt.date)
    df['TIME'] = pd.to_datetime(df['TIMESTAMP'])
    # df = df.drop(columns=[col for col in df.columns if df[col].nunique() == 1] + ['RELATIVEPOSITION'])
    return df

dfTrain = pd.read_csv("/Users/ryann_/Library/CloudStorage/OneDrive-NationalUniversityofSingapore/NUS/Y3.2/DSA3101/Prokect/IOT/TrainingData.csv")
dfValid = pd.read_csv("/Users/ryann_/Library/CloudStorage/OneDrive-NationalUniversityofSingapore/NUS/Y3.2/DSA3101/Prokect/IOT/ValidationData.csv")
df = pd.concat([dfTrain, dfValid])
df = load_and_preprocess(df)