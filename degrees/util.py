import networkx as nx
import matplotlib.pyplot as plt

class Node():
    def __init__(self, person_id, parent, movie_id):
        self.__person_id = person_id
        self.__parent = parent
        self.__movie_id = movie_id
        
    def get_person_id(self):
        return self.__person_id
    
    def get_movie_id(self):
        return self.__movie_id
    
    def get_parent(self):
        return self.__parent


class QueueFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.get_person_id == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Graph():
    
    def __init__(self, edges, path):
        self.__G = nx.Graph()
        edges_names = list(edges)
        self.__G.add_edges_from(edges_names)
        self.__edges = edges
        
        self.__color_map = []
        for node in self.__G:
            if node in path:
                self.__color_map.append("green")
            else:
                self.__color_map.append("blue")
        
    def draw_graph(self, file):    
        pos = nx.spring_layout(self.__G)
        plt.figure(figsize=(50,50))
        nx.draw(self.__G, pos, node_color=self.__color_map, with_labels=True)
        nx.draw_networkx_edge_labels(self.__G, pos, edge_labels=self.__edges)
        plt.axis("off")
        plt.savefig(file)
        plt.show()
        

