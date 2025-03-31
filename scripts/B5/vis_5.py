from Imports import plt, sns
from LoadData import df

df_floor_2 = df[df['FLOOR'] == 2]

df_floor_2_drilled = df_floor_2[df_floor_2['DATE'] == '2013-06-20'].reset_index(drop=True)
columns_to_drop = [col for col in df_floor_2_drilled.columns if df_floor_2_drilled[col].nunique() == 1]
df_floor_2_drilled = df_floor_2_drilled.drop(columns=columns_to_drop).drop(columns = ['RELATIVEPOSITION'])
# print(df_floor_2_drilled)
sns.scatterplot(data = df_floor_2_drilled, y = "LATITUDE", x = "LONGITUDE")
sns.kdeplot(data = df_floor_2_drilled, x = "LONGITUDE", y = "LATITUDE", cmap = "coolwarm")
#plt.plot(df_ave["LONGITUDE"], df_ave["LATITUDE"])
# sns.lineplot(data = df_ave, x = "LONGITUDE", y = "LATITUDE")

plt.xticks(rotation = 45)
plt.title("Heatmap of crowd density across building 1 and 2 throughout 2013-06-20")
plt.show()