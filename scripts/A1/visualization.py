import matplotlib.pyplot as plt
import seaborn as sns

def plot_staffing(staff_schedules, month, day, rain, public_holiday):
    """Plot optimized staffing schedules."""
    staff_schedule_rides, staff_schedule_eatery, staff_schedule_merch, staff_schedule_general = staff_schedules
    
    plot_data_rides = staff_schedule_rides[
        (staff_schedule_rides['Month'] == month) & 
        (staff_schedule_rides["Day"] == day)
    ]
    plot_data_eatery = staff_schedule_eatery[
        (staff_schedule_eatery['Month'] == month) & 
        (staff_schedule_eatery["Day"] == day)
    ]
    plot_data_merch = staff_schedule_merch[
        (staff_schedule_merch['Month'] == month) & 
        (staff_schedule_merch["Day"] == day)
    ]
    plot_data_general = staff_schedule_general[
        (staff_schedule_general['Month'] == month) & 
        (staff_schedule_general["Day"] == day)
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle(
        f"Staffing Schedules for {day} in {month}, "
        f"Rain: {'Yes' if rain else 'No'}, "
        f"Public Holiday: {'Yes' if public_holiday else 'No'}",
        fontsize=16
    )

    ax1 = axes[0, 0]
    sns.barplot(data=plot_data_rides, x='Hour', y='Staff', hue='Staff', palette='viridis', ax=ax1)
    ax1.set_title("Rides Staffing")
    ax1.set_xlabel("Hour")
    ax1.set_ylabel("Staff")

    ax2 = axes[0, 1]
    sns.barplot(data=plot_data_eatery, x='Hour', y='Staff', hue='Staff', palette='viridis', ax=ax2)
    ax2.set_title("Eatery Staffing")
    ax2.set_xlabel("Hour")
    ax2.set_ylabel("Staff")

    ax3 = axes[1, 0]
    sns.barplot(data=plot_data_merch, x='Hour', y='Staff', hue='Staff', palette='viridis', ax=ax3)
    ax3.set_title("Merchandise Staffing")
    ax3.set_xlabel("Hour")
    ax3.set_ylabel("Staff")

    ax4 = axes[1, 1]
    sns.barplot(data=plot_data_general, x='Hour', y='Staff', hue='Staff', palette='viridis', ax=ax4)
    ax4.set_title("General Services Staffing")
    ax4.set_xlabel("Hour")
    ax4.set_ylabel("Staff")

    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    return fig