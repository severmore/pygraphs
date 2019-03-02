import matplotlib.pyplot as plt


def covering_visualisation(gen, stations, points):
    fig, ax = plt.subplots(figsize=(8, 8))

    ax.set_xlim(0, gen.area[0])
    ax.set_ylim(0, gen.area[1])

    x_grid = list()
    y_grid = list()

    x_max = int(gen.area[0] // gen.grid[0])
    y_max = int(gen.area[1] // gen.grid[1])

    for i in range(0, x_max):
        x_grid.append(gen.grid[0] * i)

    for i in range(0, y_max):
        y_grid.append(gen.grid[1] * i)

    ax.set_xticks(x_grid)
    ax.set_yticks(y_grid)

    ax.grid(True)

    def get_circle(point, radius, color):
        return plt.Circle((point[0]*gen.cell[0], point[1]*gen.cell[0]), radius, fc=color)

    def get_blue_color(index):
        return 0, 0, 1 - ((index + 1) / len(stations))

    for i, station in enumerate(stations):
        ax.add_artist(
            get_circle(
                (station.get_x(), station.get_y()),
                station.radius,
                get_blue_color(i)
            )
        )

    for point in points:
        ax.add_artist(get_circle(point, 3, 'r'))

    fig.savefig('../covering/visualisation/covering.png')