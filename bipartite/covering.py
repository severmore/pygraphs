import random
import matplotlib.pyplot as plt
from bipartite.binary_heap import BinaryHeap
from bipartite.generating import Geo


class Point:
    def __init__(self, point=(0, 0), radius=0):
        self.x = point[0]
        self.y = point[1]
        self.radius = radius

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Station:
    def __init__(self, position=Point((0, 0), 0), radius=0, conn=0, cost=0):
        self.position = position
        self.radius = radius
        self.conn = conn
        self.cost = cost

    def __compare__(self, other):
        """
        it can be more complex function, while it is only division
        of coverage on cost of station
        :param other:
        :return:
        """
        return self.radius / self.cost >= other.radius / self.cost

    def __eq__(self, other):
        if other is None:
            return False
        return self.__compare__(other) and other.__compare__(self)

    def __lt__(self, other):
        if other is None:
            return False
        return not self.__compare__(other)

    def __gt__(self, other):
        if other is None:
            return
        return self.__compare__(other)

    def get_position(self):
        return self.position

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
    def __init__(self, area, gateway_point, stations_conf, geo):
        self.area = area
        self.gateway_point = gateway_point

        self.geo = geo
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
        # discrete variant
        self.available_points = list()

        # all points where stations can be placed
        self.points = list()
        for point in geo.get_places():
            self.points.append(Point(point))

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

        if point.x - 2 * radius > 0:
            points.append(Point(point=(point.x - 2 * radius, point.y)))

        if point.x + 2 * radius < max_x:
            points.append(Point(point=(point.x + 2 * radius, point.y)))

        if point.y - 2 * radius > 0:
            points.append(Point(point=(point.x, point.y - 2 * radius)))

        if point.y + 2 * radius < max_y:
            points.append(Point(point=(point.x, point.y + 2 * radius)))

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

        max_station_efficiency = 0
        station_to_put = stations[0]
        point_to_put = None

        for station in stations:
            for point in points:

                station_efficiency = self.station_efficiency(station, point)

                if station_efficiency > max_station_efficiency:
                    station_to_put = station
                    point_to_put = point
                    max_station_efficiency = station_efficiency

        # TODO refactoring
        if point_to_put is not None:
            self.execute_put_station_to_point(station_to_put, point_to_put, max_station_efficiency * station_to_put.cost)

    def station_efficiency(self, station, point):
        """
        This method determines what station more suitable foe this point
        :param point:
        :param station:
        :return:
        """

        station_covering = self.calculate_coveraged_area(station, point)

        return station_covering / station.cost

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

        self.coveraged_area += coveraged_area

    def recalculate_points(self, placed_station, point):
        aval_points = self.available_points
        points = self.points

        conn = placed_station.conn

        up_border = point.y + conn
        down_border = point.y - conn

        right_border = point.x + conn
        left_border = point.x - conn

        add_points = list()

        # TODO refactoring
        for p in points:
            if (
                    point.x >= left_border and point.x <= right_border and
                    up_border >= point.y >= down_border
            ):
                add_points.append(p)

        for p in add_points:
            aval_points.append(p)
            points.remove(p)

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

        # put gateway into first available station
        point = self.available_points[0]

        coveraged_area = self.calculate_coveraged_area(gateway, point)

        self.execute_put_station_to_point(gateway, point, coveraged_area)


def covering_visualisation(area, stations):
    fig, ax = plt.subplots()

    ax.set_xlim(0, area[0])
    ax.set_ylim(0, area[1])

    def get_circle(point, radius):
        return plt.Circle((point.x, point.y), radius)

    for station in stations:
        ax.add_artist(get_circle(station.get_position(), station.radius))

    fig.savefig('../visualisation/covering.png')


if __name__ == '__main__':
    """
        In the begining we generate points 
        after that generate covering  
    """
    # available min distance between stations
    r_point_min = 100

    # available max distance between stations
    r_point_max = 200

    # area to cover
    area = (800, 800)

    # points count
    points_count = 10

    gen = Geo(r_point_min, r_point_max, area, (25, 25))(points_count)

    points = gen.get_places()

    covering = AverageCover((100, 100), Point((0, 0), 0), (100, 1, 10), points)

    # execute covering
    covering()

    for station in covering.placed_stations:
        print('STATION')
        print(station.get_x(), station.get_y(), station.radius)

    covering_visualisation((100, 100), covering.placed_stations)