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
    
    def __init__(self, edges):
        self.__G = nx.Graph()
        self.__G.add_edges_from(edges)
        
    def draw_graph(self, file):
        '''pos=nx.get_node_attributes(self.__G,'pos')
        nx.draw(self.__G,pos)
        labels = nx.get_edge_attributes(self.__G,'weight')
        nx.draw_networkx_edge_labels(self.__G,pos,edge_labels=labels)
        nx.draw_networkx_labels(self.__G, pos)
        plt.savefig(file)    '''
        nx.draw(self.__G, with_labels=True)
        plt.savefig(file)
        

