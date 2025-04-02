# Overview
This sub-project contains Python scripts for subquestion B3, which seeks to allocate resources efficiently for demand variability.

## Scripts
### 1. `data_preparation.py`
This script contains the class `DataPreparer`, to prepare multiple types of data by reading data from CSV files and processing them for further analysis. The data includes:
* **Attendance Data**: Guest attendance on specific dates.
* **Waiting Times Data**: Waiting times for various attractions.
* **Reservation Data**: Reservation data from HPG and AIR systems.
* **Retail Data**: Retail data concerning peak visitor counts during specific hours.
* **Park Data**: Data on park guest traffic during different hours of the day.
* **Weather Data**: Weather data based on location, including rainfall.”

1. **`__init__`**:
* Initializes the class with the file paths for the various datasets and other required parameters, such as latitude, longitude, and date range.
2. **`prepare_attendance_data`**:
* Reads attendance data from a CSV file, drops duplicates, and handles negative attendance values by setting them to zero.
* Standardizes the attendance by calculating the mean and standard deviation for each facility and year, and computes the standardized attendance score.
3. **`prepare_waiting_times`**:
* Combines multiple waiting time files into a single DataFrame and processes the date and hour columns.
* Filters out negative guest count values and returns a cleaned DataFrame with relevant columns.
4. **`prepare_reserve_data`**:
* Combines HPG and AIR reservation data into hourly aggregates.
* Reservations are aggregated per hour for both systems and the mean number of visitors per hour is computed for each.
5. **`prepare_retail_data`**:
* Reads retail data and extracts relevant columns, such as the peak visitor count by hour and day.
6. **`prepare_park_data`**:
* Processes park-specific data, adjusting the hour and computing the difference in peak guest counts from the previous day.
7. **`prepare_weather_data`**:
* Uses the Meteostat API to fetch weather data (specifically rainfall) for the given geographic location and date range.
* The data is cleaned by filling missing values and creating a binary "Rainy" column indicating whether it rained on a given day.

### 2. `adjusters.py`
This script contains the class `DemandAdjusters`, containing methods to generate adjusters based on attendance data, waiting times, reservations, retail activity, park traffic, weather, public holidays, and rainfall. These adjusters are used to modify demand predictions based on historical data.

1. **`__init__`**:
* Initializes the class with various datasets (attendance, waiting times, reservations, retail, park data, weather data) required for generating demand adjusters
2. **`create_month_day_adjuster`**:
* Creates an adjuster based on the mean attendance for each month and day of the week. The adjuster is calculated as the percentage difference from the overall average attendance, used to modify demand predictions for specific days.
3. **`create_hourly_rides_adjuster`**:
* Uses waiting times data to generate an hourly adjuster for rides based on the average number of guests carried per hour. The adjuster is computed based on the percentage difference from the overall mean.
4. **`create_hourly_eatery_adjuster`**:
* Merges HPG and AIR reservation data to create an hourly adjuster for eateries. It calculates the percentage difference in reservation counts for each hour and combines them into a single adjuster for the eatery's demand.
5. **`create_hourly_merch_adjuster`**:
* Uses retail data to create an hourly adjuster for merchandise sales. The adjuster is based on the peak merchandise activity (peak guest counts) for each hour of the day, relative to the overall average.
6. **`create_hourly_general_adjuster`**:
* Generates an hourly adjuster for general services (e.g., guest services, maintenance) using park data. The adjuster is calculated based on the difference in the peak guest counts for each hour compared to the overall average.
7. **`create_public_holiday_adjuster`**:
* Creates an adjuster for public holidays using attendance data. It compares attendance on holidays versus non-holidays for two parks (PortAventura World and Tivoli Gardens) in Spain and Denmark. The final adjuster reflects the impact of public holidays on guest attendance.
8. **`create_rain_adjuster`**:
* Creates an adjuster based on weather data, specifically rainfall. It calculates the impact of rainy days on the total number of guests carried, comparing the mean attendance on rainy versus non-rainy days.

### 3. `optimization_model.py`
This script contains the class `StaffingOptimizer`, to perform staffing optimization. The model aims to minimize total staff while ensuring that staffing levels meet demand.

#### **Decision Variables:**
For each hour *h* (9 AM to 10 PM) and each category *c* (Rides, Eatery, Merchandise, General Service): 
$$
S_{h,c} \geq 0
$$
where *S*<sub>*h,c*</sub> represents the number of staff needed at hour *h* for category *c*.


#### **Demand Calculation:**
The adjusted demand for each category is calculated as:
$$
D_{h,c} = B \times M_m \times H_h^c \times P_p \times R_r
$$
where:
- *B* = base demand (10,000)
- *M*<sub>*m*</sub> = month and day multiplier (depends on *(m,d)*)
- *H*<sub>h</sub><sup>c</sup> = hourly multiplier for category *c* at hour *h*
- *P*<sub>*p*</sub> = public holiday multiplier
- *R*<sub>*r*</sub> = rain multiplier

#### **Staffing Constraints:**
Each staffing category has a specific requirement per unit demand:
$$
S_{h, \text{Rides}} \geq \frac{D_{h, \text{Rides}}}{30}
$$
$$
S_{h, \text{Eatery}} \geq \frac{D_{h, \text{Eatery}}}{30}
$$
$$
S_{h, \text{Merch}} \geq \frac{D_{h, \text{Merch}}}{30}
$$
$$
S_{h, \text{General}} \geq \frac{D_{h, \text{General}}}{50}
$$

#### **Objective Function:**
The goal is to minimize the total staffing:
$$
\min \sum_{h=9}^{22} \left( S_{h, \text{Rides}} + S_{h, \text{Eatery}} + S_{h, \text{Merch}} + S_{h, \text{General}} \right)
$$

#### **Optimization Problem:**
$$
\min_{S_{h,c}} \quad \sum_{h=9}^{22} S_{h, \text{Total}}
$$
subject to
$$
S_{h,c} \geq \frac{D_{h,c}}{K_c}, \quad \forall h, c
$$
$$
S_{h,c} \geq 0, \quad \forall h, c
$$
where *K*<sub>c</sub> is the staff-to-demand ratio (30 for Rides, Eatery, Merchandise; 50 for General).

### 4. `visualization.py`
This script contains the `plot_staffing` function, to generate a set of bar plots for the optimized staffing schedules across 4 categories (rides, eateries, merchandise, general services) based on the given inputs: month, day, rain (boolean), and public holiday (boolean).

#### 1. **Input Parameters**:
* `staff_schedules`: A tuple containing four DataFrames: `staff_schedule_rides`, `staff_schedule_eatery`, `staff_schedule_merch`, and `staff_schedule_general`. Each DataFrame contains the optimized staffing data for a particular category.
* `month`: The month for which the staffing is being plotted.
* `day`: The day of the month for which the staffing is being plotted.
* `rain`: A boolean value representing whether it is a rainy day or not.
* `public_holiday`: A boolean value indicating if it is a public holiday.

#### 2. **Filtering Data**:
* For each category (rides, eatery, merchandise, and general services), the function filters the staff schedules to only include rows corresponding to the selected `month` and `day`.

#### 3. **Plotting**:
* A 2x2 grid of subplots is created, with each subplot corresponding to one of the categories (rides, eateries, merchandise, and general services).
* `sns.barplot` is used to plot the staffing data for each category, with the x-axis representing the hour of the day (9 AM to 10 PM) and the y-axis representing the number of staff required for that hour.
* The `hue='Staff'` argument in `sns.barplot` helps in coloring the bars based on staffing levels, which can visually highlight the changes in staffing.
* Titles and axis labels are added to each subplot for clarity.

#### 4. **Figure Customization**:
* The `fig.suptitle` method sets the overall title of the figure, which includes the selected `month`, `day`, and the rain/public holiday conditions.
* `plt.tight_layout()` adjusts the subplot layout to minimize overlap, and `plt.subplots_adjust(top=0.92)` ensures the title is not obstructed by the plots.

#### 5. **Return**:
 * The function returns the `fig` object, which contains the entire plot.

## Data References
* `attendance.csv` and `waiting_times.csv`: https://www.kaggle.com/datasets/ayushtankha/hackathon?resource=download 
* `air_reserve.csv` and `hpg_reserve.csv`: https://www.kaggle.com/c/recruit-restaurant-visitor-forecasting/data?select=air_reserve.csv.zip 
* `retail_daily_hourly`: Yodobashi Akiba in https://besttime.app/app/Japan/Tokyo/?page=2& 
* `park_daily_hourly_peaks`: Tokyo Disneyland in https://besttime.app/app/Japan/Tokyo/?page=0&