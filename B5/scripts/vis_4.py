from Imports import plt, sns
from LoadData import df

df_grouped = df.groupby(['DATE', 'BUILDINGID'])['USERID'].nunique().reset_index()

def user_plot():
    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the bar chart using seaborn
    sns.barplot(data=df_grouped, x='DATE', y='USERID', hue='BUILDINGID', dodge=True, ax=ax)

    # Add labels and title
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Users")
    ax.set_title("Number of Users in Each Building per Day")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.legend(title="Building ID")
    return fig, ax