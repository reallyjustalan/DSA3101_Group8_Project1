from optimisation import *
from objects import *
from cleaning import *
from heatmap import *
from simulations import *
import requests
from io import StringIO

#running the file

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


start_simulation_run(ringmodel, tivoli_attr_ranking, 13)