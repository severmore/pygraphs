from covering.stations_generator import *
from bipartite.generating import Geo
from covering.covering_helper import *
from covering.utils import *
from covering.visualisation import *
import covering.CONFIG as config
import itertools


class FullSelectiveCover:

    def __init__(self, stations, geo):
        self.geo = geo
        self.stations = stations

        self.points = geo.get_places()
        self.placed_stations = list()

    def __call__(self):
        geo = self.geo
        self.points = list()

        for point in geo.get_places():
            self.points.append(point)

        possible_variants = list(itertools.permutations(self.points))
        current_coverage = 0
        optimal_coverage_points = list()

        for arrange in possible_variants:
            covering = self.calculate_coverage(arrange)
            if len(covering) > current_coverage:
                current_coverage = len(covering)
                optimal_coverage_points = arrange

        for index, point in enumerate(optimal_coverage_points):
            stations[index].set_position(point)

        self.coveraged_area = current_coverage
        self.placed_stations = stations

    def calculate_coverage(self, points):
        stations = self.stations
        coverage = set()

        for index, point in enumerate(points):
            covering_points = self.calculate_one_station(point, stations[index])
            for cov_point in covering_points:
                    coverage.add(cov_point)

        return coverage

    def calculate_one_station(self, point, station):
        radius = int( station.radius // self.geo.cell[0])
        coverage_points = set()

        border_left_x = 0
        border_right_x = self.geo.grid[0]
        border_up_y = self.geo.grid[0]
        border_down_y = 0

        if point[0] - radius > border_left_x:
            border_left_x = point[0] - radius

        if point[0] + radius < border_right_x:
            border_right_x = point[0] + radius

        if point[1] + radius < border_up_y:
            border_up_y = point[1] + radius

        if point[1] - radius > border_down_y:
            border_down_y = point[1] - radius

        for x in range (int(border_left_x), int(border_right_x)):
            for y in range(int(border_down_y), int(border_up_y)):
                coverage_points.add((x, y))

        return coverage_points


class AverageCover:
    """
    area - tuple (int, int) - area to cover
    stations - list of stations
    """
    def __init__(self, stations, geo):

        self.geo = geo
        self.stations_count = len(stations)

        # stations to put
        self.stations = stations

        # station that are placed
        # when station is placed it is removed from
        # stations list and is putted into placed_stations
        self.placed_stations = list()

        # points where stations can be placed
        # discrete variant
        self.available_points = list()

        # points that are coverage
        # in the begining this list is empty
        self.coverage_points = set()

        # all points where stations can be placed
        self.points = geo.get_places()

        self.available_points.append(self.points[0])

        # coveraged points by stations radius
        # this list is used to find point which
        # are covered by station radius
        self.placed_points = list()

        # all coveraged area
        self.coveraged_area = 0

    def __call__(self):
        self.put_gateway()
        #TODO hack!!!
        while len(self.stations) > 0 and len(self.available_points) > 0:
            self.put_station_to_point()

        self.coveraged_area = len(self.coverage_points)

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

        max_station_efficiency = {'efficiency': 0, 'points': {}}
        station_to_put = stations[0]
        point_to_put = None

        for station in stations:
            for point in avail_points:

                station_efficiency = self.station_efficiency(station, point)

                if station_efficiency.get('efficiency') >= max_station_efficiency.get('efficiency'):
                    station_to_put = station
                    point_to_put = point
                    max_station_efficiency = station_efficiency

        # TODO refactoring
        if point_to_put is not None:
            self.execute_put_station_to_point(station_to_put, point_to_put, max_station_efficiency)

    def station_efficiency(self, station, point):
        """
        This method determines what station more suitable foe this point
        :param point:
        :param station:
        :return: map {efficiency, points}
        """

        station_covering = calculate_coverage_area(self.geo, station, point)
        return {'efficiency': len(station_covering), 'points': station_covering}

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

        for point1 in coveraged_area.get('points'):
            self.coverage_points.add(point1)

        self.coveraged_area += coveraged_area.get('efficiency')

    def recalculate_points(self, placed_station):
        all_points = self.points

        station_point = placed_station.get_position()

        for p in all_points:
            if self.geo.distance(station_point, p) <= placed_station.conn**2:
                if p not in self.available_points and p not in self.placed_points:
                    self.available_points.append(p)

        self.available_points.remove(station_point)

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


if __name__ == '__main__':
    """
        In the begining we generate points 
        after that generate covering  
    """
    # available min distance between stations

    gen = Geo(config.DISTANCE_MIN,
              config.DISTANCE_MAX,
              config.AREA,
              config.GRID)

    gen(config.POINTS_COUNT)

    points = gen.get_places()

    stations = generate_stations(config.STATIONS_COUNT, (
        config.MIN_BACKBONE_RADIUS, config.MAX_BACKBONE_RADIUS), (
        config.MIN_COVERING_RADIUS, config.MAX_COVERING_RADIUS)
                                 )

    covering = FullSelectiveCover(stations, gen)

    # execute covering
    # start_time = time.time()
    covering()
    # print('Execution Full Selective algorithm takes: ' + str(time.time() - start_time))
    #for station in covering.placed_stations:
    #    print('STATION')
    #    print(station.get_x(), station.get_y(), station.radius)
    print(covering.coveraged_area)
    covering_visualisation(gen, covering.placed_stations, points, 'full_covering')

    covering = AverageCover(stations, gen)
    covering()
    print(covering.coveraged_area)
    covering_visualisation(gen, covering.placed_stations, points, 'covering')
