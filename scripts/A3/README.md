## Overview

This sub-project contains Python scripts for analyzing visitor patterns and cost-profit relationships at Disney California Adventure theme park. The analysis uses three main datasets:

1. **Theme Park Attraction Visits Dataset** (`userVisits-DisneyCaliforniaAdventure.csv`)
2. **List of Attractions/POIs Dataset** (`POI-DisneyCaliforniaAdventure.csv`)
3. **Attraction/POI Cost-Profit Table Dataset** (`costProfCat-DisneyCaliforniaAdventurePOI-all.csv`)

## Scripts

### 1. `journey_analysis.py`

This script analyzes visitor movement patterns through the park and identifies opportunity zones for business improvement.

#### Key Features:
- Loads and preprocesses POI and visitor sequence data
- Visualizes attraction locations on an interactive map
- Identifies common journey patterns between attractions
- Creates visitor flow network diagrams
- Identifies underutilized "opportunity zones" near popular attractions

#### Main Functions:
- `load_data()`: Loads and merges POI and visitor data
- `plot_poi_map()`: Creates interactive map of all attractions
- `analyze_journey_patterns()`: Identifies common visitor sequences
- `create_flow_network()`: Builds network graph of visitor flows
- `analyze_opportunity_zones()`: Finds underutilized areas near top attractions
- `get_business_insights()`: Returns precomputed business recommendations

### 2. `cost_profit_analysis.py`

This script analyzes the cost-effectiveness and popularity of different attraction routes.

#### Key Features:
- Calculates cost-effectiveness metrics (popularity/distance)
- Visualizes distance vs popularity relationships
- Identifies most efficient and popular routes
- Provides insights about attraction categories

#### Main Functions:
- `load_cost_profit_data()`: Loads and preprocesses cost-profit data
- `plot_cost_profit_scatter()`: Creates scatter plot of distance vs popularity
- `get_cost_profit_insights()`: Returns top efficient/popular routes and insights

## Data Structure

All datasets use semicolon (`;`) as delimiter. Key columns include:

- **Visitor Data**: `photoID`, `userID`, `dateTaken`, `poiID`, `seqID`
- **POI Data**: `poiID`, `poiName`, `lat`, `long`, `theme`, `rideDuration`
- **Cost-Profit Data**: `from`, `to`, `cost`, `profit`, `theme`

## Usage

1. Install required packages:
   ```
   pip install pandas matplotlib seaborn networkx plotly scipy
   ```

2. Run analysis scripts:
   ```python
   # For visitor journey analysis
   from journey_analysis import load_data, plot_poi_map, analyze_journey_patterns
   poi, seq, df = load_data('POI-DisneyCaliforniaAdventure.csv', 'userVisits-DisneyCaliforniaAdventure.csv')
   
   # For cost-profit analysis
   from cost_profit_analysis import load_cost_profit_data, plot_cost_profit_scatter
   df = load_cost_profit_data('costProfCat-DisneyCaliforniaAdventurePOI-all.csv')
   ```

## Business Insights

The analysis reveals several key patterns:
- Popular attraction pairings (e.g., Radiator Springs Racers with Disney Junior)
- Family-oriented visitor flow trends
- Cost-effective routes dominated by Family/Show combinations
- Underutilized opportunity zones near top attractions

## References

If you use these datasets, please cite:
```bibtex
@INPROCEEDINGS { lim-sigir17,
   AUTHOR = {Kwan Hui Lim and Jeffrey Chan and Shanika Karunasekera and Christopher Leckie},
   TITLE = {Personalized Itinerary Recommendation with Queuing Time Awareness},
   BOOKTITLE = {Proceedings of the 40th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR'17)},
   PAGES = {325-334},
   YEAR = {2017}
}
```
