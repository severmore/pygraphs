import random


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