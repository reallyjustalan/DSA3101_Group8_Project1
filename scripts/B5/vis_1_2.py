from Imports import plt
from LoadData import df
# Plot the points
plt.scatter(df["LONGITUDE"], df["LATITUDE"], color='red', marker='o')

# Labels and title
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Map of Locations")
plt.grid()

# Show the map
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['LONGITUDE'], df['LATITUDE'], df['FLOOR'])

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.view_init(elev=10, azim=-82)  # Adjust elevation and azimuth angles

plt.show()