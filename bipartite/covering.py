import random


class Point:
    def __init__(self, point=(0, 0), radius=0):
        self.x = point[0]
        self.y = point[1]
        self.radius = radius


def generate_radius(min_value, max_value):
    return random.randint(min_value, max_value)


"""
    This function is used to cover available zones by
    similar stations with similar covering radius
    :param
        geo - instance of class (Geo)
        available_stations_count - number of available stations (int)
        stations_radius - distance covering by one station (float)
        point_radius - distance to cover in one point (float)
"""

def cover_current_geo_map(geo,
                          available_stations_count,
                          staions_radius,
                          point_radius,
                          gateway_point
                          ):

    generated_places = geo.get_places()
    min_radius = geo.r_disable
    max_radius = geo.r_allowed

    # generate place, that should be covered
    generated_places = generated_places.map(lambda place:
                                            Point(place,
                                                  generate_radius(min_radius, max_radius)))

    # generate similar stations
    generated_stations = []

    for i in range(0, available_stations_count):
        generated_stations.append(Point(radius=point_radius))

