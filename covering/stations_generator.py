from covering.utils import generate_radius, Station


def generate_stations(count, radius):
    """
    method generates stations
    generate list of stations and set it into self.stations
    """
    min_radius = radius[0]
    max_radius = radius[1]
    stations = list()

    for i in range(0, count - 1):
        stations.append(Station(radius=10, conn=generate_radius(min_radius, max_radius)))
    return stations