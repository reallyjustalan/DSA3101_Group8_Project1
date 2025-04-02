from optimisation import *
from objects import *
from cleaning import *
from heatmap import *
from simulations import *
import requests
from all_heatmaps_simulated import *
from io import StringIO
from all_optimisation_sample_provider import *
#running the file


#Sample Set up
ringmodel = ThemeParkGridModel(9,9,(2,2),(6,6))
github_csv_url = "https://raw.githubusercontent.com/NotInvalidUsername/DSA3101_Group8_Project1/alan_bean/data/tivoli_attr_ranking.csv"

# Fetch the CSV content
response = requests.get(github_csv_url)
if response.status_code == 200:
    tivoli_attr_ranking = pd.read_csv(StringIO(response.text))
    print("CSV loaded successfully!")
    print(tivoli_attr_ranking.head())  # Display first 5 rows
else:
    print(f"Failed to fetch CSV. HTTP Status: {response.status_code}")

#Single run of a single model
full_simulation_run(ringmodel, tivoli_attr_ranking, 13)


#Sample bulk creation of multiple models for the streamlit app

#Creation of databases
downloads_path = str(Path.home() / "Downloads")
simulations_dir = os.path.join(downloads_path, 'heatmap')
simulations_dir_2 = os.path.join(downloads_path, 'simulation')
os.makedirs(simulations_dir, exist_ok=True)

#Creation of models
MODEL_CONFIGS = {
    'model1': {  # Small park with central restricted area
        'width': 9,
        'height': 9,
        'restricted_bottom_left': (2, 2),
        'restricted_top_right': (6, 6)
    },
    'model2': {  # Medium park with no restricted areas
        'width': 9,
        'height': 9,
        'restricted_bottom_left': None,
        'restricted_top_right': None
    },
    'model3': {  # Large park with multiple restricted zones
        'width': 15,
        'height': 15,
        'restricted_bottom_left': (1, 2),
        'restricted_top_right': (3, 6)
    }
}
#Creates 10 iterations of different optimisation paths for 11 parameters (indicated within tivoli_attr_ranking)
run_all_simulations(MODEL_CONFIGS, tivoli_attr_ranking, simulations_dir_2)

# Run all simulations of heatmaps for the 3 different parks. runs the first 70 steps for the 11 different parameters
run_all_simulations_heatmap(MODEL_CONFIGS, tivoli_attr_ranking,simulations_dir)
    

