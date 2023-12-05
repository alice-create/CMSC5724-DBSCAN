'''
Created on Nov 20, 2023
@author: yychen
'''
import numpy as np

class Cluster(object):
    def __init__(self, name, dim):
        self.name = name
        self.dim = dim
        self.points = []

    def add_point(self, point):
        self.points.append(point)

    def get_points(self):
        return self.points

    def erase(self):
        self.points = []

    def get_X(self):
        return [p["value"][0] for p in self.points]

    def get_Y(self):
        return [p["value"][1] for p in self.points]

    def has(self, point):
        return point in self.points

    def __str__(self):
        return "{}: {} points".format(self.name, len(self.points))

