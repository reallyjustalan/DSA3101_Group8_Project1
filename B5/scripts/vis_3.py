from Imports import plt
from LoadData import df

dfgrouped = df.groupby(["BUILDINGID", "FLOOR"]).size().reset_index(name="num_access_points")
pivot_df = dfgrouped.pivot(index="FLOOR", columns="BUILDINGID", values="num_access_points")

# Plot the bar chart
pivot_df.plot(kind="bar", figsize=(10, 6))
"""
# Add labels and title
plt.xlabel("Floor")
plt.ylabel("Number of Access Points")
plt.title("Access Points per Floor for Each Building")
plt.legend(title="Building ID")

plt.show()"""

def wap_distrubution():
    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the bar chart
    pivot_df.plot(kind="bar", ax=ax)

    # Add labels and title
    ax.set_xlabel("Floor")
    ax.set_ylabel("Number of Access Points")
    ax.set_title("Access Points per Floor for Each Building")
    ax.legend(title="Building ID")

    return fig, ax