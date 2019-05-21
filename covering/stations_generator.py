from covering.utils import generate_radius, Station


def generate_stations(count, radius, cover_radius):

    min_radius = radius[0]
    max_radius = radius[1]

    min_cover = cover_radius[0]
    max_cover = cover_radius[1]

    stations = list()

    for _ in range(0, count):
        stations.append(Station(radius=generate_radius(min_cover, max_cover),
                                conn=generate_radius(min_radius, max_radius)))
    return stations