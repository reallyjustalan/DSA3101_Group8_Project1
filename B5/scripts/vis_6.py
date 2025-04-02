from Imports import plt, sns, pd
from custom_functions import mean_exclude_100
from vis_5 import df_floor_2_drilled

df_floor_2_drilled_indexed = df_floor_2_drilled.set_index('TIMESTAMP')
columns_to_drop = [col for col in df_floor_2_drilled_indexed.columns if df_floor_2_drilled_indexed[col].nunique() == 1]
df_floor_2_drilled_indexed = df_floor_2_drilled_indexed.drop(columns=columns_to_drop).drop(columns = ['BUILDINGID'])

df_ave = df_floor_2_drilled_indexed.groupby(pd.Grouper(freq = '20T')).agg(mean_exclude_100).fillna(100)
df_ave = df_ave[df_ave['PHONEID'] != 100]
"""
sns.scatterplot(data = df_floor_2_drilled, y = "LATITUDE", x = "LONGITUDE")
sns.kdeplot(data = df_floor_2_drilled, x = "LONGITUDE", y = "LATITUDE", cmap = "coolwarm")
sns.lineplot(data = df_ave, x = "LONGITUDE", y = "LATITUDE", color = 'red')
plt.xticks(rotation = 45)
plt.title("Heatmap of crowd density across building 1 and 2 throughout 2013-06-20")
plt.show()"""

def create_heatmap_trend():
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Scatter plot (optional, can be removed if too cluttered)
    sns.scatterplot(data=df_floor_2_drilled, y="LATITUDE", x="LONGITUDE", ax=ax, alpha=0.5, color='black', s=10)
    
    # Hexbin heatmap (adjust gridsize for resolution)
    hexbin = ax.hexbin(
        x=df_floor_2_drilled["LONGITUDE"],
        y=df_floor_2_drilled["LATITUDE"],
        gridsize=30,  # Adjust for resolution
        cmap="coolwarm",
        bins='log',  # Use log scale if data is highly skewed
        alpha=0.7
    )
    
    # Add colorbar
    plt.colorbar(hexbin, ax=ax, label='Density')
    
    # Line plot (if needed)
    sns.lineplot(data=df_ave, x="LONGITUDE", y="LATITUDE", ax=ax, color='green', linewidth=2)
    
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_title("Spatial Heatmap of Crowd Density (2013-06-20)")

    return fig, ax

"""
def create_heatmap_trend():
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Contour-based heatmap
    sns.kdeplot(
        data=df_floor_2_drilled,
        x="LONGITUDE",
        y="LATITUDE",
        levels=20,  # Number of contour levels
        cmap="coolwarm",
        fill=True,  # Filled contours
        alpha=0.7,
        thresh=0.1,  # Threshold for lowest contour
        ax=ax
    )
    
    # Scatter plot (optional)
    sns.scatterplot(data=df_floor_2_drilled, y="LATITUDE", x="LONGITUDE", ax=ax, alpha=0.3, color='black', s=10)
    
    # Line plot
    sns.lineplot(data=df_ave, x="LONGITUDE", y="LATITUDE", ax=ax, color='green', linewidth=2)
    
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_title("Contour Heatmap of Crowd Density (2013-06-20)")
    return fig, ax
    """