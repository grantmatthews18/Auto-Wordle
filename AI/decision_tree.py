import decision_tree as dt

class Node():
    def __init__(self, new_cost = "null"):
        self._node_ptr_arr = []
        self._cost = new_cost
        self._best_path = []

    def set_cost(self, new_cost):
        self._cost = new_cost

    def get_cost(self):
        return(self._cost)

    def add_node(self, new_node = None):
        if(new_node == None):
            self._node_ptr_arr.append(Node())
        else:
            self._node_ptr_arr.append(new_node)

    def get_node(self, index):
        return(self._node_ptr_arr[index])

    def num_nodes(self):
        return(len(self._node_ptr_arr))

    def add_to_best_path(self, choice):
        self._best_path.insert(0,choice)

    def get_best_path(self):
        return(self._best_path)
