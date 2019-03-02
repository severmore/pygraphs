from covering.utils import Point


def calculate_coveraged_area(geo, station, point):
    """
    Calculate count of points
    and return list of points
    :param station:
    :param point:
    :return:
    """
    x = point.x
    y = point.y

    # while only square grid
    radius = int(station.radius)

    coverage_points = list()

    # borders for calculations
    border_left_x = 0
    border_right_x = geo.grid[0] - 1
    border_up_y = geo.grid[0] - 1
    border_down_y = 0

    if point.x - radius > border_left_x:
        border_left_x = point.x - radius

    if point.x + radius < border_right_x:
        border_right_x = point.x + radius

    if point.y + radius < border_up_y:
        border_up_y = point.y + radius

    if point.y - radius > border_down_y:
        border_down_y = point.y - radius

    for x1 in range(border_left_x, border_right_x):
        for y1 in range(border_down_y, border_up_y):
            if geo.distance((x, y), (x1, y1)) <= radius ** 2:
                coverage_points.append(Point((x1, y1)))

    return coverage_points
