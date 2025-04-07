from Imports import pd, os
from custom_functions import load_and_preprocess

# Get the current script's directory
script_dir = os.path.dirname(__file__)

# Construct relative path to the data directory
data_dir = os.path.join(script_dir, '../../data/B5')

# Create file path and load dfTrain
filename = 'TrainingData.csv'  
file_path = os.path.join(data_dir, filename)
dfTrain = pd.read_csv(file_path)

# Create file path and load dfValid
filename = 'ValidationData.csv'  
file_path = os.path.join(data_dir, filename)
dfValid = pd.read_csv(file_path)

# Combine the CSV files
df = pd.concat([dfTrain, dfValid])

# Preprocess CSV files
df = load_and_preprocess(df)