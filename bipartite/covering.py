import random
import matplotlib.pyplot as plt
from bipartite.generating import Geo


class Point:
    def __init__(self, point=(0, 0), radius=0):
        self.x = point[0]
        self.y = point[1]
        self.radius = radius

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Station:
    def __init__(self, position=Point((0, 0), 0), radius=0, conn=0, cost=1):
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

        # points that are coverage
        # in the begining this list is empty
        self.coverage_points = list()

        # all points where stations can be placed
        self.points = list()
        for point in geo.get_places():
            self.points.append(Point(point))

        self.available_points.append(self.points[0])

        # coveraged points by stations radius
        # this list is used to find point which
        # are covered by station radius
        self.placed_points = list()

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
            self.stations.append(Station(radius=10, conn=generate_radius(min_radius, max_radius)))

    def put_station_to_point(self):
        """
        choose the most covering station from available stations
        and out into place and remove from available stations
        for current point
        :param point: Point instance
        :return:
        """
        stations = self.stations
        avail_points = self.available_points

        max_station_efficiency = 0
        station_to_put = stations[0]
        point_to_put = None
        station_efficiency = None

        for station in stations:
            for point in avail_points:

                station_efficiency = self.station_efficiency(station, point)

                if station_efficiency.get('efficiency') > max_station_efficiency:
                    station_to_put = station
                    point_to_put = point
                    max_station_efficiency = station_efficiency.get('efficiency')

        # TODO refactoring
        if point_to_put is not None:
            self.execute_put_station_to_point(station_to_put, point_to_put, station_efficiency)

    def station_efficiency(self, station, point):
        """
        This method determines what station more suitable foe this point
        :param point:
        :param station:
        :return: map {efficiency, points}
        """

        station_covering = self.calculate_coveraged_area(station, point)
        return {'efficiency': len(station_covering) / station.cost, 'points': station_covering}

    def execute_put_station_to_point(self, station, point, coveraged_area):
        """
        his method replace station from station list to placed_stations
        add available points to points list and increment coveraged area
        :param coveraged_area:
        :param station:
        :param point:
        :param max_coveraged_area:
        :return:
        """
        self.placed_points.append(point)
        self.placed_stations.append(station)
        self.stations.remove(station)
        station.set_position(point)
        self.recalculate_points(station)
        self.coverage_points += coveraged_area.get('points')
        self.coveraged_area += coveraged_area.get('efficiency') * station.cost

    def recalculate_points(self, placed_station):
        all_points = self.points

        station_point = placed_station.get_position()

        for p in all_points:
            if self.geo.distance((station_point.x, station_point.y), (p.x, p.y)) <= placed_station.conn**2:
                if p not in self.available_points and p not in self.placed_points:
                    self.available_points.append(p)

        self.available_points.remove(station_point)

    def calculate_coveraged_area(self, station, point):
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

        # birders for calculations
        border_left_x = 0
        border_right_x = self.geo.grid[0] - 1
        border_up_y = self.geo.grid[0] - 1
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
                if self.geo.distance((x, y), (x1, y1)) <= radius**2:
                    coverage_points.append(Point((x1, y1)))

        return coverage_points

    def put_gateway(self):
        """
        in current case this function put first station
        to point(0, 0)
        :return:
        """
        gateway = self.stations[0]
        point = self.available_points[0]
        coveraged_area = self.station_efficiency(gateway, point)

        self.execute_put_station_to_point(gateway, point, coveraged_area)


def covering_visualisation(area, stations):
    fig, ax = plt.subplots()

    ax.set_xlim(0, area[0])
    ax.set_ylim(0, area[1])

    def get_circle(point, radius):
        return plt.Circle((point.x*gen.cell[0], point.y*gen.cell[0]), radius)

    for station in stations:
        ax.add_artist(get_circle(station.get_position(), station.radius))

    fig.savefig('../visualisation/covering.png')


if __name__ == '__main__':
    """
        In the begining we generate points 
        after that generate covering  
    """
    # available min distance between stations
    r_point_min = 20

    # available max distance between stations
    r_point_max = 30

    # area to cover
    area = (100, 100)

    # points count
    points_count = 10

    gen = Geo(r_point_min, r_point_max, area, (5, 5))

    gen(points_count)

    points = gen.get_places()

    covering = AverageCover(area, Point((0, 0), 0), (8, 30, 50), gen)

    # execute covering
    covering()

    for station in covering.placed_stations:
        print('STATION')
        print(station.get_x(), station.get_y(), station.radius)

    covering_visualisation(area, covering.placed_stations)