from Imports import plt, sns
from LoadData import df

df_grouped = df.groupby(['DATE', 'BUILDINGID'])['USERID'].nunique().reset_index()
# Plot
plt.figure(figsize=(12, 6))
sns.barplot(data=df_grouped, x='DATE', y='USERID', hue='BUILDINGID', dodge=True)

# Labels
plt.xlabel("Date")
plt.ylabel("Number of Users")
plt.title("Number of Users in Each Building per Day")
plt.xticks(rotation=90)
plt.legend(title="Building ID")

# Show plot
plt.show()