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


