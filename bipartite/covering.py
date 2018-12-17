import random
import matplotlib.pyplot as plt
from bipartite.binary_heap import BinaryHeap


class Point:
    def __init__(self, point=(0, 0), radius=0):
        self.x = point[0]
        self.y = point[1]
        self.radius = radius

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Station:
    def __init__(self, position=Point((0, 0), 0), radius=0):
        self.position = position
        self.radius = radius

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return self.radius == other.radius

    def __lt__(self, other):
        if other is None:
            return False
        else:
            return self.radius < other.radius

    def __gt__(self, other):
        if other is None:
            return
        else:
            return self.radius > other.radius

    def set_position(self, position):
        self.position = position

    def get_x(self):
        return self.position.x

    def set_x(self, x):
        self.position.x = x

    def get_y(self):
        return self.position.y

    def set_y(self, y):
        self.position.y = y


def generate_radius(min_value, max_value):
    return random.randint(min_value, max_value)


class AverageCover:
    """
    area - tuple (int, int) - area to cover
    gateway_point Point object
    stations_conf - tuple(int, int, int) with params: count, min_radius, max_radius accordingly
    """
    def __init__(self, area, gateway_point, stations_conf):
        self.area = area
        self.gateway_point = gateway_point

        self.stations_count = stations_conf[0]
        self.min_radius = stations_conf[1]
        self.max_radius = stations_conf[2]

        # stations to put
        self.stations = list()

        # station that are placed
        # when station is placed it is removed from
        # stations list and is putted into placed_stations
        self.placed_stations = list()

        # points where stations can be placed
        self.available_points = list()

        # coveraged points by stations radius
        # this list is used to find point which
        # are covered by station radius
        self.caveraged_point = list()

        # all coveraged area
        self.coveraged_area = 0

    def __call__(self, *args, **kwargs):
        self.generate_stations()
        self.put_gateway()
        while len(self.stations) > 0:
            self.put_station_to_point()

    def generate_stations(self):
        """
        method generates stations
        generate list of stations and set it into self.stations
        """
        count = self.stations_count
        min_radius = self.min_radius
        max_radius = self.max_radius

        for i in range(0, count - 1):
            self.stations.append(Station(radius=generate_radius(min_radius, max_radius)))

    def get_available_points_in_step(self, point, radius):
        """
        Now this function return 4 point:
        left, right, up and down available from point
        with coverage radius = radius
        """
        points = list()

        max_x = self.area[0]
        max_y = self.area[1]

        if point.x - radius > 0:
            points.append(Point(point=(point.x - radius, point.y)))

        if point.x + radius < max_x:
            points.append(Point(point=(point.x + radius, point.y)))

        if point.y - radius > 0:
            points.append(Point(point=(point.x, point.y - radius)))

        if point.y + radius < max_y:
            points.append(Point(point=(point.x, point.y + radius)))

        return points

    def put_station_to_point(self):
        """
        choose the most covering station from available stations
        and out into place and remove from available stations
        for current point
        :param point: Point instance
        :return:
        """
        stations = self.stations
        points = self.available_points

        max_coveraged_area = 0
        station_to_put = None
        point_to_put = None

        for station in stations:
            for point in points:
                coveraged_area = self.calculate_coveraged_area(station, point)
                if coveraged_area > max_coveraged_area:
                    station_to_put = station
                    point_to_put = point
                    max_coveraged_area = coveraged_area

        self.execute_put_station_to_point(station_to_put, point_to_put, max_coveraged_area)

    def execute_put_station_to_point(self, station, point, coveraged_area):
        """
        his method replace station from station list to placed_stations
        add available points to points list and increment coveraged area
        :param station:
        :param point:
        :param max_coveraged_area:
        :return:
        """
        self.placed_stations.append(station)

        self.stations.remove(station)

        station.set_position(point)

        self.available_points.remove(point)
        # concat two lists
        self.available_points = self.available_points + self.get_available_points_in_step(point, station.radius)

        self.coveraged_area += coveraged_area

    def calculate_coveraged_area(self, station, point):
        x = point.x
        y = point.y

        radius = station.radius

        coveraged_x = 0
        coveraged_y = 0

        border_x = self.area[0]
        border_y = self.area[1]

        # TODO refactoring
        if x - radius < 0:
            coveraged_x += x
        else:
            coveraged_x += radius
        if x + radius > border_x:
            coveraged_x += border_x - x
        else:
            coveraged_x += radius

        if y - radius < 0:
            coveraged_y += y
        else:
            coveraged_y += radius
        if y + radius > border_y:
            coveraged_y += border_y - y
        else:
            coveraged_y += radius

        return coveraged_x * coveraged_y

    def put_gateway(self):
        """
        in current case this function put first station
        to point(0, 0)
        :return:
        """
        gateway = self.stations[0]
        point = Point((0, 0), 0)
        self.available_points.append(point)
        coveraged_area = self.calculate_coveraged_area(gateway, point)

        self.execute_put_station_to_point(gateway, point, coveraged_area)


if __name__ == '__main__':
    covering = AverageCover((20, 20), Point((0, 0), 0), (10, 1, 4))
    covering()

    for station in covering.placed_stations:
        print('STATION')
        print(station.get_x(), station.get_y(), station.radius)