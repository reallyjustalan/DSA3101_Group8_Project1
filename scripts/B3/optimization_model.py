import cvxpy as cp
import pandas as pd
import calendar

class StaffingOptimizer:
    def __init__(self, adjusters, base_demand):
        self.adjusters = adjusters
        self.base_demand = base_demand
        
    def optimize_staffing(self, month, day, rain, public_holiday):
        """Optimize staffing based on given parameters."""
        month_num = list(calendar.month_name).index(month) if month in calendar.month_name else None
        month_day_key = (month_num, day)
        
        # Initialize decision variables
        staff_rides = {(month_day_key, hour): cp.Variable(nonneg=True) for hour in range(9, 23)}
        staff_eatery = {(month_day_key, hour): cp.Variable(nonneg=True) for hour in range(9, 23)}
        staff_merch = {(month_day_key, hour): cp.Variable(nonneg=True) for hour in range(9, 23)}
        staff_general = {(month_day_key, hour): cp.Variable(nonneg=True) for hour in range(9, 23)}
        
        # Get multipliers
        month_day_multiplier = self.adjusters['month_day'].get(month_day_key, 1)
        public_holiday_multiplier = self.adjusters['public_holiday'][int(public_holiday)]
        rain_multiplier = self.adjusters['rain'][int(rain)]
        
        # Constraints
        constraints = []
        for hour in range(9, 23):
            hour_multiplier_rides = self.adjusters['hour_rides'].get(hour, 1)
            hour_multiplier_eatery = self.adjusters['hour_eatery'].get(hour, 1)
            hour_multiplier_merch = self.adjusters['hour_merch'].get(hour, 1)
            hour_multiplier_general = self.adjusters['hour_general'].get(hour, 1)
            
            adjusted_demand_rides = (
                self.base_demand * month_day_multiplier * hour_multiplier_rides * 
                public_holiday_multiplier * rain_multiplier
            )
            adjusted_demand_eatery = (
                self.base_demand * month_day_multiplier * hour_multiplier_eatery * 
                public_holiday_multiplier * rain_multiplier
            )
            adjusted_demand_merch = (
                self.base_demand * month_day_multiplier * hour_multiplier_merch * 
                public_holiday_multiplier * rain_multiplier
            )
            adjusted_demand_general = (
                self.base_demand * month_day_multiplier * hour_multiplier_general * 
                public_holiday_multiplier * rain_multiplier
            )
            
            # Set constraints
            constraints.append(staff_rides[(month_day_key, hour)] >= adjusted_demand_rides / 30)
            constraints.append(staff_eatery[(month_day_key, hour)] >= adjusted_demand_eatery / 30)
            constraints.append(staff_merch[(month_day_key, hour)] >= adjusted_demand_merch / 30)
            constraints.append(staff_general[(month_day_key, hour)] >= adjusted_demand_general / 50)
        
        # Objective function
        total_staff = (
            cp.sum([staff_rides[(month_day_key, hour)] for hour in range(9, 23)]) +
            cp.sum([staff_eatery[(month_day_key, hour)] for hour in range(9, 23)]) +
            cp.sum([staff_merch[(month_day_key, hour)] for hour in range(9, 23)]) +
            cp.sum([staff_general[(month_day_key, hour)] for hour in range(9, 23)])
        )
        
        objective = cp.Minimize(total_staff)
        problem = cp.Problem(objective, constraints)
        problem.solve()
        
        if problem.status == cp.OPTIMAL:
            optimized_ride_staffing = [
                (month, day, hour, "Rides", staff_rides[(month_day_key, hour)].value, rain, public_holiday) 
                for hour in range(9,23)
            ]
            optimized_eatery_staffing = [
                (month, day, hour, "Eatery", staff_eatery[(month_day_key, hour)].value, rain, public_holiday) 
                for hour in range(9,23)
            ]
            optimized_merch_staffing = [
                (month, day, hour, "Merchandise", staff_merch[(month_day_key, hour)].value, rain, public_holiday) 
                for hour in range(9,23)
            ]
            optimized_general_staffing = [
                (month, day, hour, "General", staff_general[(month_day_key, hour)].value, rain, public_holiday) 
                for hour in range(9,23)
            ]
            
            staff_schedule_rides = pd.DataFrame(
                optimized_ride_staffing, 
                columns=['Month', 'Day', 'Hour', 'Category', 'Staff', 'Rain', 'Public Holiday']
            )
            staff_schedule_eatery = pd.DataFrame(
                optimized_eatery_staffing, 
                columns=['Month', 'Day', 'Hour', 'Category', 'Staff', 'Rain', 'Public Holiday']
            )
            staff_schedule_merch = pd.DataFrame(
                optimized_merch_staffing, 
                columns=['Month', 'Day', 'Hour', 'Category', 'Staff', 'Rain', 'Public Holiday']
            )
            staff_schedule_general = pd.DataFrame(
                optimized_general_staffing, 
                columns=['Month', 'Day', 'Hour', 'Category', 'Staff', 'Rain', 'Public Holiday']
            )
            
            return staff_schedule_rides, staff_schedule_eatery, staff_schedule_merch, staff_schedule_general
        else:
            raise ValueError("Optimization failed with status:", problem.status)