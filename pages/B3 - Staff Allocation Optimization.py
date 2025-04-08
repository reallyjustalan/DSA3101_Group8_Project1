import os
import streamlit as st
from pathlib import Path
import pandas as pd
import calendar

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Optimization Model", "Business Recommendations"])

### Page 1: Optimization Model ###
if page == "Optimization Model":
    st.title("Staff Allocation Optimization")

    st.write("## Business Question")
    st.markdown("""
                **How can we optimize staff allocation in a theme park at any given time while minimizing overall staffing levels?**

                To do this, optimization model will be informed by guest demand patterns.
                """)

    with st.expander("How the optimization model works"):
        st.write("### Guest Demand Preparation")
        st.markdown("""
            Using historical attendance and demand data, adjustment multipliers are calculated by dividing observed demand by baseline demand (mean across all months, days, and hours) for each factor: month-day, hour, rain, and public holidays. The adjustment multiplier by the hour is computed separately for rides, eateries, merchandise, and general services, each service category follows different demand patterns through the day.
            Using this approach, minimal data is stored. The only data stored are dictionaries for each of the adjustment categories.
        """)

        st.write("### Optimization Model")
        st.latex(r"""
        \textbf{Decision Variables:} \\
        \text{For each hour } h \in \{9 \text{ AM}, \dots, 10 \text{ PM}\}, \text{ and each category } c \in \{\text{Rides, Eatery, Merchandise, General}\}: \\
        S_{h,c} \geq 0 \quad \text{(Number of staff needed at hour } h \text{ for category } c)

        \\[1em]
        \textbf{Demand Calculation:} \\
        D_{h,c} = B \times M_m \times H_h^c \times P_p \times R_r \\
        \text{where:} \\
        B = \text{base demand (as set by user)} \\
        M_m = \text{month and day multiplier} \\
        H_h^c = \text{hourly multiplier for category } c \text{ at hour } h \\
        P_p = \text{public holiday multiplier} \\
        R_r = \text{rain multiplier}

        \\[1em]
        \textbf{Staffing Constraints:} \\
        S_{h, \text{Rides}} \geq \frac{D_{h, \text{Rides}}}{30} \\
        S_{h, \text{Eatery}} \geq \frac{D_{h, \text{Eatery}}}{30} \\
        S_{h, \text{Merch}} \geq \frac{D_{h, \text{Merch}}}{30} \\
        S_{h, \text{General}} \geq \frac{D_{h, \text{General}}}{50}

        \\[1em]
        \textbf{Objective Function:} \\
        \min \sum_{h=9}^{22} \left( S_{h, \text{Rides}} + S_{h, \text{Eatery}} + S_{h, \text{Merch}} + S_{h, \text{General}} \right)

        \\[1em]
        \textbf{Optimization Problem:} \\
        \min_{S_{h,c}} \quad \sum_{h=9}^{22} S_{h, \text{Total}} \\
        \text{subject to:} \\
        S_{h,c} \geq \frac{D_{h,c}}{K_c}, \quad \forall h, c \\
        S_{h,c} \geq 0, \quad \forall h, c \\
        \text{where } K_c = 
        \begin{cases}
        30, & \text{if } c \in \{\text{Rides, Eatery, Merchandise}\} \\
        50, & \text{if } c = \text{General}
        \end{cases}
        """)

    # Use simpler relative paths for data files
    data_dir = Path("data") / "B3"

    # Load all data files using the simplified path structure
    month_day_filepath = data_dir / "adjust_month_day.csv"
    adjust_month_day = pd.read_csv(month_day_filepath)
    month_day_adjuster = adjust_month_day.set_index(['Month', 'Day_of_Week'])['adjuster_month_day'].to_dict()

    hour_rides_filepath = data_dir / "adjust_hour_rides.csv"
    adjust_hour_rides = pd.read_csv(hour_rides_filepath)
    hour_adjuster_rides = adjust_hour_rides.set_index('DEB_TIME_HOUR')['adjuster_hourly_rides'].to_dict()

    hour_eatery_filepath = data_dir / "adjust_hour_eatery.csv"
    adjust_hour_eatery = pd.read_csv(hour_eatery_filepath)
    hour_adjuster_eatery = adjust_hour_eatery.set_index('hour')['adjuster'].to_dict()

    hour_merch_filepath = data_dir / "adjust_hour_merch.csv"
    adjust_hour_merch = pd.read_csv(hour_merch_filepath)
    hour_adjuster_merch = adjust_hour_merch.set_index('hour')['adjuster'].to_dict()

    hour_general_filepath = data_dir / "adjust_hour_general.csv"
    adjust_hour_general = pd.read_csv(hour_general_filepath)
    hour_adjuster_general = adjust_hour_general.set_index('hour_adjusted')['adjuster'].to_dict()

    public_holiday_filepath = data_dir / "adjust_public_holiday.csv"
    adjust_public_holiday = pd.read_csv(public_holiday_filepath)
    hour_adjuster_pubhol = adjust_public_holiday.set_index('status')['adjuster'].to_dict()

    rain_filepath = data_dir / "adjust_rain.csv"
    adjust_rain = pd.read_csv(rain_filepath)
    rain_adjuster = adjust_rain.set_index('Rainy')['adjuster_rain'].to_dict()

    # Construct adjusters dictionary
    adjusters = {
        'month_day': month_day_adjuster,
        'hour_rides': hour_adjuster_rides,
        'hour_eatery': hour_adjuster_eatery,
        'hour_merch': hour_adjuster_merch,
        'hour_general': hour_adjuster_general,
        'public_holiday': hour_adjuster_pubhol,
        'rain': rain_adjuster
    }

    # Add scripts folder to path and import StaffingOptimizer
    from scripts.B3.optimization_model import StaffingOptimizer
    from scripts.B3.visualization import plot_staffing

    # User inputs
    base_demand = st.number_input("Enter Estimated Park Attendance for the Day", min_value=1, max_value=1000000, value=10000)
    month = st.selectbox("Select Month", list(calendar.month_name[1:]))
    day = st.selectbox("Select Day of the Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], index=0)
    rain = st.radio("Is it forecasted to rain?", ["No", "Yes"]) == "Yes"
    public_holiday = st.radio("Is it a public holiday?", ["No", "Yes"]) == "Yes"

    # Run optimization when user clicks the button
    if st.button("Optimize Staffing"):
        optimizer = StaffingOptimizer(adjusters, base_demand)
        staff_schedule_rides, staff_schedule_eatery, staff_schedule_merch, staff_schedule_general = optimizer.optimize_staffing(month, day, rain, public_holiday)

        # Generate and display visualization
        fig = plot_staffing([staff_schedule_rides, staff_schedule_eatery, staff_schedule_merch, staff_schedule_general], month, day, rain, public_holiday)
        st.pyplot(fig)

        # Show optimized staffing schedules in tabular form
        st.write("### Optimized Staffing Schedules")
        with st.expander("Rides"):
            st.dataframe(staff_schedule_rides)
        
        with st.expander("Eateries"):
            st.dataframe(staff_schedule_eatery)
        
        with st.expander("Merchandise"):
            st.dataframe(staff_schedule_merch)

        with st.expander("General"):
            st.dataframe(staff_schedule_general)

### Page 2: Business Recommendations ###
elif page == "Business Recommendations":

    st.title("Staff Allocation Optimization")

    with st.expander("Insights"):
        st.markdown("""
            As seen from the optimized staffing plots, guest demand is indeed a major factor that should be taken into account when seeking to optimize staffing. Guest demand patterns vary substantially through the day across the 4 service categories, and overall park demand is greatly influenced by the month, day of the week, and public holidays. Rain has a minimal impact on total park attendance and hence overall park staffing, but would surely become a major factor when allocating staff to sheltered or unsheltered attractions.
                    
            This model enables maximized workforce utilization while minimizing overall labour costs. It can also inform operational decisions, such as adjusting attraction hours to reduce running services during periods of low demand. This leads to costs savings not only in labour, but also in utilities and maintenance, ensuring resources are deployed only when and where they are most needed.
        """)

    with st.expander("Limitations"):
        st.markdown("""
        This model operates under the simplified assumption that optimal staffing aligns directly with guest demand.
        
        In practice, workforce planning is far more complex, and factors such as specialized roles within service categories, wages and labour availability need to be taken into account for staffing to be optimal for the business. These factors were not taken into account as they are highly context-specific, while this model aims to be easily generalizable. In its current form, the model should only be used as a guiding recommendation rather than a definitive staffing plan.
        """)