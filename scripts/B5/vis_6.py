from Imports import plt, sns, pd
from custom_functions import mean_exclude_100
from vis_5 import df_floor_2_drilled

df_floor_2_drilled_indexed = df_floor_2_drilled.set_index('TIMESTAMP')
columns_to_drop = [col for col in df_floor_2_drilled_indexed.columns if df_floor_2_drilled_indexed[col].nunique() == 1]
df_floor_2_drilled_indexed = df_floor_2_drilled_indexed.drop(columns=columns_to_drop).drop(columns = ['BUILDINGID'])

df_ave = df_floor_2_drilled_indexed.groupby(pd.Grouper(freq = '20T')).agg(mean_exclude_100).fillna(100)
df_ave = df_ave[df_ave['PHONEID'] != 100]

sns.scatterplot(data = df_floor_2_drilled, y = "LATITUDE", x = "LONGITUDE")
sns.kdeplot(data = df_floor_2_drilled, x = "LONGITUDE", y = "LATITUDE", cmap = "coolwarm")
sns.lineplot(data = df_ave, x = "LONGITUDE", y = "LATITUDE", color = 'red')
plt.xticks(rotation = 45)
plt.title("Heatmap of crowd density across building 1 and 2 throughout 2013-06-20")
plt.show()