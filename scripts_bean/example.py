from optimisation import *
from objects import *
from cleaning import *
from heatmap import *
from simulations import *

#running the file

ringmodel = ThemeParkGridModel(9,9,(2,2),(6,6))
tivoli_attr_ranking = pd.read_csv('tivoli_attr_ranking.csv')

start_simulation_run(ringmodel, tivoli_attr_ranking, 13)
