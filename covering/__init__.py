import matplotlib.pyplot as plt
from covering.stations_generator import *
from bipartite.generating import Geo
from covering.covering_helper import *
from covering.utils import *
import covering.CONFIG as config


class AverageCover:
    """
    area - tuple (int, int) - area to cover
    gateway_point Point object
    stations_conf - tuple(int, int, int) with params: count, min_radius, max_radius accordingly
    """
    def __init__(self, gateway_point, stations_conf, geo):

        self.gateway_point = gateway_point
        self.geo = geo
        self.stations_count = stations_conf[0]
        self.min_radius = stations_conf[1]
        self.max_radius = stations_conf[2]

        self.cover_min_radius = stations_conf[3]
        self.cover_max_radius = stations_conf[4]

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
        self.stations = generate_stations(self.stations_count,
                                          (self.min_radius,
                                           self.max_radius
                                           ),
                                          (40, 100))
        self.put_gateway()
        while len(self.stations) > 0:
            self.put_station_to_point()

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

        station_covering = calculate_coveraged_area(self.geo, station, point)
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


def covering_visualisation(area, stations, points):
    fig, ax = plt.subplots(figsize=(8, 8))

    ax.set_xlim(0, area[0])
    ax.set_ylim(0, area[1])

    def get_circle(point, radius, color):
        return plt.Circle((point[0]*gen.cell[0], point[1]*gen.cell[0]), radius, fc=color)

    for station in stations:
        ax.add_artist(get_circle((station.get_x(), station.get_y()), station.radius, 'b'))

    for point in points:
        ax.add_artist(get_circle(point, 1, 'r'))


    fig.savefig('../visualisation/covering.png')


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

    covering = AverageCover(Point((0, 0), 0),
                            (
                                config.STATIONS_COUNT,
                                config.MIN_BACKBONE_RADIUS,
                                config.MAX_BACKBONE_RADIUS,
                                config.MIN_COVERING_RADIUS,
                                config.MAX_COVERING_RADIUS
                             ),
                            gen)

    # execute covering
    covering()

    for station in covering.placed_stations:
        print('STATION')
        print(station.get_x(), station.get_y(), station.radius)

    covering_visualisation(config.AREA, covering.placed_stations, points)