'''
Created on Nov 20, 2023
@author: yychen
'''

from cluster import Cluster
import matplotlib.pyplot as plt
from math import *

class Scanner:

    def __init__(self, config):
        self.eps = config["eps"]
        self.min_pts = config["min_pts"]
        self.dim = config["dim"]
        self.clusters = set()
        self.cluster_num = 0
        self.visited = []
        self.color = ['b','g','r']


    def dbscan(self, data):
        self.init_params()
        self.data = data

        fig = plt.figure()

        axis_proj = 'rectilinear'

        ax = fig.add_subplot(111, projection=axis_proj)

        #default noise cluster
        noise = Cluster('Noise', self.dim)
        self.clusters.add(noise)

        for point in data:
            if point not in self.visited:
                self.visited.append(point)
                neighbour_pts = self.region_query(point)
                if len(neighbour_pts) < self.min_pts:
                    noise.add_point(point)
                else:
                    name = 'cluster-{}'.format(self.cluster_num)
                    new_cluster = Cluster(name, self.dim)

                    self.cluster_num += 1
                    self.expend_cluster(new_cluster, point, neighbour_pts)


                    ax.scatter(new_cluster.get_X(), new_cluster.get_Y(), c=self.color[self.cluster_num % len(self.color)],
                                   marker='o', label=name)

                    # ax.hold(True)

        if len(noise.get_points()) != 0:

            ax.scatter(noise.get_X(), noise.get_Y(), marker='x', label=noise.name)

        print("Number of clusters found: %d" % self.cluster_num)

        # ax.hold(False)
        ax.legend(loc='lower left')
        ax.grid(True)
        plt.title(r'DBSCAN Clustering', fontsize=18)
        plt.suptitle(r'eps:{} min_pts:{}'.format(self.eps, self.min_pts))
        plt.savefig("visualization.png")
        plt.show()

    def expend_cluster(self, cluster, point, neighbour_pts):
        cluster.add_point(point)
        for p in neighbour_pts:
            if p not in self.visited:
                self.visited.append(p)
                np = self.region_query(p)
                if len(np) >= self.min_pts:
                    for n in np:
                        if n not in neighbour_pts:
                            neighbour_pts.append(n)

                for other_cluster in self.clusters:
                    if not other_cluster.has(p):
                        if not cluster.has(p):
                            cluster.add_point(p)

                if self.cluster_num == 0:
                    if not cluster.has(p):
                        cluster.add_point(p)

        self.clusters.add(cluster)


    def get_distance(self, from_point, to_point):
        p1 = [from_point['value'][k] for k in range(self.dim)]
        p2 = [to_point['value'][k] for k in range(self.dim)]
        x = (p1[0] - p2[0]) ** 2
        y = (p1[1] - p2[1]) ** 2
        distance = sqrt(x + y)
        return distance

    def region_query(self, point):
        result = []
        for d_point in self.data:
            if d_point != point:
                if self.get_distance(d_point, point) <= self.eps:
                    result.append(d_point)
        return result

    def export(self, export_file="cluster_dump"):
        with open(export_file, 'w') as dump_file:
            for cluster in self.clusters:
                for point in cluster.points:
                    csv_point = ','.join(map(str, point['value']))
                    dump_file.write("%s;%s\n" % (csv_point, cluster.name))
        print("Cluster dumped at: %s" % export_file)

    def init_params(self):
        self.clusters = set()
        self.cluster_num = 0
        self.visited = []


