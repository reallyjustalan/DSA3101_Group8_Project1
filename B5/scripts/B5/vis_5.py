from Imports import plt, sns
from LoadData import df

df_floor_2 = df[df['FLOOR'] == 2]

df_floor_2_drilled = df_floor_2[df_floor_2['DATE'] == '2013-06-20'].reset_index(drop=True)
columns_to_drop = [col for col in df_floor_2_drilled.columns if df_floor_2_drilled[col].nunique() == 1]
df_floor_2_drilled = df_floor_2_drilled.drop(columns=columns_to_drop).drop(columns = ['RELATIVEPOSITION'])

def create_heatmap():

    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Scatterplot (optional, can be removed if too cluttered)
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
    
    plt.colorbar(hexbin, ax=ax, label='Density')
    
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_title("Spatial Heatmap of Crowd Density (2013-06-20)")

    return fig, ax