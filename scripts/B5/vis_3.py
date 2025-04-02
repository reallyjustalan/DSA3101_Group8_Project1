from Imports import plt
from LoadData import df

dfgrouped = df.groupby(["BUILDINGID", "FLOOR"]).size().reset_index(name="num_access_points")
pivot_df = dfgrouped.pivot(index="FLOOR", columns="BUILDINGID", values="num_access_points")

pivot_df.plot(kind="bar", figsize=(10, 6))

def wap_distrubution():
    fig, ax = plt.subplots(figsize=(10, 6))

    pivot_df.plot(kind="bar", ax=ax)

    ax.set_xlabel("Floor")
    ax.set_ylabel("Number of entries")
    ax.legend(title="Building ID")

    return fig, ax