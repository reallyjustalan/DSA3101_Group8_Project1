from Imports import plt
from LoadData import df

def scatter():
    fig, ax = plt.subplots()

    ax.scatter(df["LONGITUDE"], df["LATITUDE"], color='red', marker='o')

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Map of Locations")
    ax.grid()
    return fig, ax

def plot3d():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df['LONGITUDE'], df['LATITUDE'], df['FLOOR'])

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.view_init(elev=10, azim=-82)  # Adjust elevation and azimuth angles

    return fig, ax