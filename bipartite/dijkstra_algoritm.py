import math
import sys

from bipartite.graph import WeightGraph
from bipartite.binary_heap import BinaryHeap

"""
    This function realize Dijkstra algorithm
    for search the shortest way via weight function.
    For implementation of queue with priority the binary tree is used
    We need to ave else one structure in parallel with bae structure
"""

"""
    Constant for initialization 
    of max weight of edge
"""

MAX_WEIGHT = sys.maxsize


class DijkstraAlgorithm():

    def __init__(self, graph, start_index, end_index):
        """
            Algorithm is build by:
            @:param graph is instance of WeightGraph class
            @:param start_index (int) is index of vertex from algorithm starts
            @:param end_vertex (int) is index of vertex where algorithm finish
        """
        self.initial_weight_structure = dict()
        self.initial_helper_structure = BinaryHeap()
        self.graph = graph
        self.start_index = start_index
        self.end_index = end_index
        """
            Store graph edges
        """
        self.edges = graph.edges
        """
            This field contains determined vertex by which path is build
        """
        self.path_structure = dict()

        self.result = None

    def __call__(self, *args, **kwargs):
        self.build_base_structure()
        self.dijkstra_algorithm()

    def build_base_structure(self):
        """
            Method initialize base key-value structure
            and in parallel initialize
            :return:
        """

        count = len(self.graph.edges)
        start_index = self.start_index

        """
            Initialization of weight structure and
            helper binary heap
        """
        for i in range(0, count - 1):
            if i == start_index:
                new_element = PathTreeNode(weigth=0, index=i)
            else:
                new_element = PathTreeNode(index=i)
            self.initial_weight_structure[i] = new_element
            self.initial_helper_structure.add_element(new_element)

    """
        Implementation of dijkstra algorithm
    """
    def dijkstra_algorithm(self):
        vertex_heap = self.initial_helper_structure
        determined_structure = dict()

        while vertex_heap.get_heap_size() > 0:
            current_vertex = vertex_heap.get_root()
            neighbor_vertexs = self.get_vertex_neighbors(current_vertex.index)
            for neighbord_vertex in neighbor_vertexs:
                self.relaxation(current_vertex, neighbord_vertex)
            determined_structure[current_vertex.index] = current_vertex
        self.result = determined_structure

    def relaxation(self, from_vertex, to_vertex):
        if from_vertex is not None and from_vertex.weight != MAX_WEIGHT and to_vertex is not None:
            edge_weight = self.get_edge_weight(from_vertex.index, to_vertex.index)
            if to_vertex.weight > edge_weight + from_vertex.weight:
                to_vertex.weight = edge_weight + from_vertex.weight
                to_vertex.parent = from_vertex.index

    def get_edge_weight(self, from_vertex, to_vertex):
        result = MAX_WEIGHT
        edges = self.edges[from_vertex]
        for edge in edges:
            if edge.to_vertex == to_vertex:
                result = edge.weight
        return result

    """
        Return list with PathTreeNode instances
        that are neighbors 
    """
    def get_vertex_neighbors(self, vertex_index):
        result = []
        node_edges = self.edges[vertex_index]
        for edge in node_edges:
            result.append(self.initial_weight_structure[edge.to_vertex])
        return result

    """
        This method is used only for debug
    """
    def get_result(self):
        keys = list(self.result.keys())
        result = []
        for key in keys:
            result.append({
                "index": key,
                "parent": self.result[key].parent,
                "weight": self.result[key].weight
            })
        return result

    """
        Return object: 
        {
            path: list() with indexes,
            weight: int weight of finded path
        }
    """
    def get_path(self):
        initial_vertexs = self.initial_weight_structure
        current_index = self.end_index

        vertexs = list()

        while current_index is not None:
            vertexs.insert(0, current_index)
            current_index = initial_vertexs[current_index].parent

        return {
            "path": vertexs,
            "weight": initial_vertexs[self.end_index].weight
        }



class PathTreeNode:
    """
        :param parent: - int number from vertex
        :param weigth: - expected weight
    """
    def __init__(self, index=0, parent=None, weigth=MAX_WEIGHT):
        self.index = index
        self.parent = parent
        self.weight = weigth

    """
        Node tree less than other if it weight MORE than other
        Reverted due to placement in binary heap
    """
    def __lt__(self, other):
        if other is None:
            return False
        else:
            return self.weight > other.weight

    """
        Node tree more than other if it weight LESS than other
        Reverted due to placement in binary heap
    """
    def __gt__(self, other):
        if other is None:
            return False
        else:
            return self.weight < other.weight

if __name__ == '__main__':
    graph = WeightGraph(edges=[(0, 1, 1), (0, 2, 1), (1, 2, 2), (2, 3, 4)])
    alg = DijkstraAlgorithm(graph, 0, 3)
    alg()
    print(alg.get_result())
    print(alg.get_path())
