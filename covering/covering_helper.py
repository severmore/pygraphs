
def calculate_coverage_area(geo, station, point):
    radius = int(station.radius // geo.cell[0])
    coverage_points = set()

    border_left_x = 0
    border_right_x = geo.grid[0]
    border_up_y = geo.grid[0]
    border_down_y = 0

    if point[0] - radius > border_left_x:
        border_left_x = point[0] - radius

    if point[0] + radius < border_right_x:
        border_right_x = point[0] + radius

    if point[1] + radius < border_up_y:
        border_up_y = point[1] + radius

    if point[1] - radius > border_down_y:
        border_down_y = point[1] - radius

    for x in range(int(border_left_x), int(border_right_x)):
        for y in range(int(border_down_y), int(border_up_y)):
            coverage_points.add((x, y))

    return coverage_points
