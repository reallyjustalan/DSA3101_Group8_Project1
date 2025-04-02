from Imports import plt, sns
from LoadData import df

df_floor_2 = df[df['FLOOR'] == 2]

df_floor_2_drilled = df_floor_2[df_floor_2['DATE'] == '2013-06-20'].reset_index(drop=True)
columns_to_drop = [col for col in df_floor_2_drilled.columns if df_floor_2_drilled[col].nunique() == 1]
df_floor_2_drilled = df_floor_2_drilled.drop(columns=columns_to_drop).drop(columns = ['RELATIVEPOSITION'])
# print(df_floor_2_drilled)

def create_heatmap():

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(data=df_floor_2_drilled, y="LATITUDE", x="LONGITUDE", ax=ax)
    sns.kdeplot(data=df_floor_2_drilled, x="LONGITUDE", y="LATITUDE", cmap="coolwarm", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_title("Heatmap of crowd density across building 1 and 2 throughout 2013-06-20")

    return fig, ax