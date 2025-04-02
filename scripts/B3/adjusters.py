import numpy as np
import holidays

class DemandAdjusters:
    def __init__(self, attendance_data=None, waiting_times=None, hpg_hourly_all_sum=None, air_hourly_all_sum=None,
                 retail_daily_hourly=None, park_daily_hourly=None, weather_merged=None):
        self.attendance_data = attendance_data
        self.waiting_times = waiting_times
        self.hpg_hourly_all_sum = hpg_hourly_all_sum
        self.air_hourly_all_sum = air_hourly_all_sum
        self.retail_daily_hourly = retail_daily_hourly
        self.park_daily_hourly = park_daily_hourly
        self.weather_merged = weather_merged

    def create_month_day_adjuster(self):
        """Create month-day adjuster from attendance data."""
        mean_month_day_attendance = self.attendance_data.groupby(["Month", "Day_of_Week"])["attendance"].mean().reset_index()
        mean_month_day_attendance.rename(columns={"attendance": "mean_month_day_attendance"}, inplace=True)
        overall_mean = mean_month_day_attendance["mean_month_day_attendance"].mean()

        mean_month_day_attendance["abs_diff_from_overall_mean"] = (
            mean_month_day_attendance["mean_month_day_attendance"] - overall_mean
        )
        mean_month_day_attendance["pct_diff_from_overall_mean"] = (
            mean_month_day_attendance["abs_diff_from_overall_mean"] / overall_mean
        )

        mean_month_day_attendance["adjuster_month_day"] = (
            1 + mean_month_day_attendance["pct_diff_from_overall_mean"]
        )

        return mean_month_day_attendance.set_index(["Month", "Day_of_Week"])["adjuster_month_day"].to_dict()

    def create_hourly_rides_adjuster(self):
        """Create hourly rides adjuster from waiting times data."""
        rides_hourly_agg = self.waiting_times.groupby("DEB_TIME_HOUR")["GUEST_CARRIED"].mean().reset_index()
        rides_hourly_agg.rename(columns={"GUEST_CARRIED": "mean_guest_carried"}, inplace=True)
        overall_mean_guest_carried = rides_hourly_agg["mean_guest_carried"].mean()

        rides_hourly_agg["abs_diff_from_overall_mean"] = (
            rides_hourly_agg["mean_guest_carried"] - overall_mean_guest_carried
        )
        rides_hourly_agg["pct_diff_from_overall_mean"] = (
            rides_hourly_agg["abs_diff_from_overall_mean"] / overall_mean_guest_carried
        )

        rides_hourly_agg["adjuster_hourly_rides"] = (
            1 + rides_hourly_agg["pct_diff_from_overall_mean"]
        )

        return rides_hourly_agg.set_index("DEB_TIME_HOUR")["adjuster_hourly_rides"].to_dict()

    def create_hourly_eatery_adjuster(self):
        """Create hourly eatery adjuster from hpg and air reserve data."""
        eatery_merging = self.hpg_hourly_all_sum.merge(
            self.air_hourly_all_sum[['hour', 'air_mean_reserve_visitors_per_hour']],
            on='hour',
            how='left'
        )

        eatery_merging['hpg_pct_diff'] = (
            (eatery_merging['hpg_mean_reserve_visitors_per_hour'] - 
             eatery_merging['hpg_mean_reserve_visitors_per_hour'].mean()) / 
            eatery_merging['hpg_mean_reserve_visitors_per_hour'].mean()
        )
        eatery_merging['air_pct_diff'] = (
            (eatery_merging['air_mean_reserve_visitors_per_hour'] - 
             eatery_merging['air_mean_reserve_visitors_per_hour'].mean()) / 
            eatery_merging['air_mean_reserve_visitors_per_hour'].mean()
        )

        eatery_ah_pct = eatery_merging[["hour", "hpg_pct_diff", "air_pct_diff"]]
        eatery_ah_pct['combined_pct_diff'] = eatery_ah_pct[['hpg_pct_diff', 'air_pct_diff']].mean(axis=1)

        eatery_ah_pct['adjuster'] = 1 + eatery_ah_pct["combined_pct_diff"]

        return eatery_ah_pct.set_index("hour")["adjuster"].to_dict()

    def create_hourly_merch_adjuster(self):
        """Create hourly merchandise adjuster from retail data."""
        mean_hourly_peak_frc = self.retail_daily_hourly.groupby("hour")["peak_frc"].mean()
        overall_mean_peak_frc = self.retail_daily_hourly["peak_frc"].mean()

        mean_hourly_peak_frc = mean_hourly_peak_frc.reset_index()
        mean_hourly_peak_frc.rename(columns={"index": "hour"}, inplace=True)
        mean_hourly_peak_frc["pct_diff"] = mean_hourly_peak_frc["peak_frc"] - overall_mean_peak_frc
        mean_hourly_peak_frc["adjuster"] = 1 + mean_hourly_peak_frc["pct_diff"]

        return mean_hourly_peak_frc.set_index("hour")["adjuster"].to_dict()

    def create_hourly_general_adjuster(self):
        """Create hourly general service adjuster from park data."""
        park_mean_hourly_peaks = self.park_daily_hourly.groupby("hour_adjusted")["peak_frc_diff"].mean()
        overall_park_mean_peaks = self.park_daily_hourly["peak_frc_diff"].mean()

        park_mean_hourly_peaks = park_mean_hourly_peaks.reset_index()
        park_mean_hourly_peaks.rename(columns={"index": "hour_adjusted"}, inplace=True)
        park_mean_hourly_peaks["pct_diff"] = park_mean_hourly_peaks["peak_frc_diff"] - overall_park_mean_peaks
        park_mean_hourly_peaks["adjuster"] = 1 + park_mean_hourly_peaks["pct_diff"]

        return park_mean_hourly_peaks.set_index("hour_adjusted")["adjuster"].to_dict()

    def create_public_holiday_adjuster(self):
        """Create public holiday adjuster from attendance data."""
        portaventura_df = self.attendance_data[self.attendance_data["FACILITY_NAME"] == "PortAventura World"]
        tivoli_df = self.attendance_data[self.attendance_data["FACILITY_NAME"] == "Tivoli Gardens"]

        spain_holidays = holidays.Spain(years=[2018, 2019, 2020, 2021, 2022])
        portaventura_df["is_holiday"] = portaventura_df["USAGE_DATE"].apply(lambda x: x in spain_holidays)

        overall_daily_attendance = portaventura_df["attendance"].mean()
        holiday_attendance = portaventura_df[portaventura_df["is_holiday"] == True]["attendance"].mean()
        non_holiday_attendance = portaventura_df[portaventura_df["is_holiday"] == False]["attendance"].mean()

        ph_adjuster_spain = (holiday_attendance - overall_daily_attendance) / overall_daily_attendance
        non_ph_adjuster_spain = (non_holiday_attendance - overall_daily_attendance) / overall_daily_attendance

        denmark_holidays = holidays.Denmark(years=[2018, 2019, 2020, 2021, 2022])
        tivoli_df["is_holiday"] = tivoli_df["USAGE_DATE"].apply(lambda x: x in denmark_holidays)

        overall_daily_attendance = tivoli_df["attendance"].mean()
        holiday_attendance = tivoli_df[tivoli_df["is_holiday"] == True]["attendance"].mean()
        non_holiday_attendance = tivoli_df[tivoli_df["is_holiday"] == False]["attendance"].mean()

        ph_adjuster_denmark = (holiday_attendance - overall_daily_attendance) / overall_daily_attendance
        non_ph_adjuster_denmark = (non_holiday_attendance - overall_daily_attendance) / overall_daily_attendance

        adjust_pubhol = 1 + (np.mean([ph_adjuster_denmark, ph_adjuster_spain]))
        adjust_no_pubhol = 1 + (np.mean([non_ph_adjuster_denmark, non_ph_adjuster_spain]))

        return {0: adjust_no_pubhol, 1: adjust_pubhol}

    def create_rain_adjuster(self):
        """Create rain adjuster from weather data."""
        mean_guests_by_rain = self.weather_merged.groupby('Rainy')['TOTAL_GUESTS_CARRIED'].mean().reset_index()
        overall_mean = self.weather_merged['TOTAL_GUESTS_CARRIED'].mean()
        mean_guests_by_rain.rename(columns={'TOTAL_GUESTS_CARRIED': 'mean_total_guests_carried'}, inplace=True)
        mean_guests_by_rain['pct_diff_from_overall'] = (
            mean_guests_by_rain['mean_total_guests_carried'] - overall_mean
        ) / overall_mean
        mean_guests_by_rain["adjuster"] = (1 + mean_guests_by_rain["pct_diff_from_overall"])

        return mean_guests_by_rain.set_index("Rainy")["adjuster"].to_dict()