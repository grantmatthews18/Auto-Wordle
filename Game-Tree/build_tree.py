import json
import copy

import multiprocessing as mp

#globals
GLOBAL_ID_CT = 0
def get_global_id():
    global GLOBAL_ID_CT
    GLOBAL_ID_CT += 1
    return(GLOBAL_ID_CT-1)

GLOBAL_ID_LOCK = mp.Lock()

POSSIBLE_RESULT_ARRAY = [('e', 'e', 'e', 'e', 'e'), ('e', 'e', 'e', 'e', 'y'), ('e', 'e', 'e', 'e', 'g'), ('e', 'e', 'e', 'y', 'e'), ('e', 'e', 'e', 'y', 'y'), ('e', 'e', 'e', 'y', 'g'), ('e', 'e', 'e', 'g', 'e'), ('e', 'e', 'e', 'g', 'y'), ('e', 'e', 'e', 'g', 'g'), ('e', 'e', 'y', 'e', 'e'), ('e', 'e', 'y', 'e', 'y'), ('e', 'e', 'y', 'e', 'g'), ('e', 'e', 'y', 'y', 'e'), ('e', 'e', 'y', 'y', 'y'), ('e', 'e', 'y', 'y', 'g'), ('e', 'e', 'y', 'g', 'e'), ('e', 'e', 'y', 'g', 'y'), ('e', 'e', 'y', 'g', 'g'), ('e', 'e', 'g', 'e', 'e'), ('e', 'e', 'g', 'e', 'y'), ('e', 'e', 'g', 'e', 'g'), ('e', 'e', 'g', 'y', 'e'), ('e', 'e', 'g', 'y', 'y'), ('e', 'e', 'g', 'y', 'g'), ('e', 'e', 'g', 'g', 'e'), ('e', 'e', 'g', 'g', 'y'), ('e', 'e', 'g', 'g', 'g'), ('e', 'y', 'e', 'e', 'e'), ('e', 'y', 'e', 'e', 'y'), ('e', 'y', 'e', 'e', 'g'), ('e', 'y', 'e', 'y', 'e'), ('e', 'y', 'e', 'y', 'y'), ('e', 'y', 'e', 'y', 'g'), ('e', 'y', 'e', 'g', 'e'), ('e', 'y', 'e', 'g', 'y'), ('e', 'y', 'e', 'g', 'g'), ('e', 'y', 'y', 'e', 'e'), ('e', 'y', 'y', 'e', 'y'), ('e', 'y', 'y', 'e', 'g'), ('e', 'y', 'y', 'y', 'e'), ('e', 'y', 'y', 'y', 'y'), ('e', 'y', 'y', 'y', 'g'), ('e', 'y', 'y', 'g', 'e'), ('e', 'y', 'y', 'g', 'y'), ('e', 'y', 'y', 'g', 'g'), ('e', 'y', 'g', 'e', 'e'), ('e', 'y', 'g', 'e', 'y'), ('e', 'y', 'g', 'e', 'g'), ('e', 'y', 'g', 'y', 'e'), ('e', 'y', 'g', 'y', 'y'), ('e', 'y', 'g', 'y', 'g'), ('e', 'y', 'g', 'g', 'e'), ('e', 'y', 'g', 'g', 'y'), ('e', 'y', 'g', 'g', 'g'), ('e', 'g', 'e', 'e', 'e'), ('e', 'g', 'e', 'e', 'y'), ('e', 'g', 'e', 'e', 'g'), ('e', 'g', 'e', 'y', 'e'), ('e', 'g', 'e', 'y', 'y'), ('e', 'g', 'e', 'y', 'g'), ('e', 'g', 'e', 'g', 'e'), ('e', 'g', 'e', 'g', 'y'), ('e', 'g', 'e', 'g', 'g'), ('e', 'g', 'y', 'e', 'e'), ('e', 'g', 'y', 'e', 'y'), ('e', 'g', 'y', 'e', 'g'), ('e', 'g', 'y', 'y', 'e'), ('e', 'g', 'y', 'y', 'y'), ('e', 'g', 'y', 'y', 'g'), ('e', 'g', 'y', 'g', 'e'), ('e', 'g', 'y', 'g', 'y'), ('e', 'g', 'y', 'g', 'g'), ('e', 'g', 'g', 'e', 'e'), ('e', 'g', 'g', 'e', 'y'), ('e', 'g', 'g', 'e', 'g'), ('e', 'g', 'g', 'y', 'e'), ('e', 'g', 'g', 'y', 'y'), ('e', 'g', 'g', 'y', 'g'), ('e', 'g', 'g', 'g', 'e'), ('e', 'g', 'g', 'g', 'y'), ('e', 'g', 'g', 'g', 'g'), ('y', 'e', 'e', 'e', 'e'), ('y', 'e', 'e', 'e', 'y'), ('y', 'e', 'e', 'e', 'g'), ('y', 'e', 'e', 'y', 'e'), ('y', 'e', 'e', 'y', 'y'), ('y', 'e', 'e', 'y', 'g'), ('y', 'e', 'e', 'g', 'e'), ('y', 'e', 'e', 'g', 'y'), ('y', 'e', 'e', 'g', 'g'), ('y', 'e', 'y', 'e', 'e'), ('y', 'e', 'y', 'e', 'y'), ('y', 'e', 'y', 'e', 'g'), ('y', 'e', 'y', 'y', 'e'), ('y', 'e', 'y', 'y', 'y'), ('y', 'e', 'y', 'y', 'g'), ('y', 'e', 'y', 'g', 'e'), ('y', 'e', 'y', 'g', 'y'), ('y', 'e', 'y', 'g', 'g'), ('y', 'e', 'g', 'e', 'e'), ('y', 'e', 'g', 'e', 'y'), ('y', 'e', 'g', 'e', 'g'), ('y', 'e', 'g', 'y', 'e'), ('y', 'e', 'g', 'y', 'y'), ('y', 'e', 'g', 'y', 'g'), ('y', 'e', 'g', 'g', 'e'), ('y', 'e', 'g', 'g', 'y'), ('y', 'e', 'g', 'g', 'g'), ('y', 'y', 'e', 'e', 'e'), ('y', 'y', 'e', 'e', 'y'), ('y', 'y', 'e', 'e', 'g'), ('y', 'y', 'e', 'y', 'e'), ('y', 'y', 'e', 'y', 'y'), ('y', 'y', 'e', 'y', 'g'), ('y', 'y', 'e', 'g', 'e'), ('y', 'y', 'e', 'g', 'y'), ('y', 'y', 'e', 'g', 'g'), ('y', 'y', 'y', 'e', 'e'), ('y', 'y', 'y', 'e', 'y'), ('y', 'y', 'y', 'e', 'g'), ('y', 'y', 'y', 'y', 'e'), ('y', 'y', 'y', 'y', 'y'), ('y', 'y', 'y', 'y', 'g'), ('y', 'y', 'y', 'g', 'e'), ('y', 'y', 'y', 'g', 'y'), ('y', 'y', 'y', 'g', 'g'), ('y', 'y', 'g', 'e', 'e'), ('y', 'y', 'g', 'e', 'y'), ('y', 'y', 'g', 'e', 'g'), ('y', 'y', 'g', 'y', 'e'), ('y', 'y', 'g', 'y', 'y'), ('y', 'y', 'g', 'y', 'g'), ('y', 'y', 'g', 'g', 'e'), ('y', 'y', 'g', 'g', 'y'), ('y', 'y', 'g', 'g', 'g'), ('y', 'g', 'e', 'e', 'e'), ('y', 'g', 'e', 'e', 'y'), ('y', 'g', 'e', 'e', 'g'), ('y', 'g', 'e', 'y', 'e'), ('y', 'g', 'e', 'y', 'y'), ('y', 'g', 'e', 'y', 'g'), ('y', 'g', 'e', 'g', 'e'), ('y', 'g', 'e', 'g', 'y'), ('y', 'g', 'e', 'g', 'g'), ('y', 'g', 'y', 'e', 'e'), ('y', 'g', 'y', 'e', 'y'), ('y', 'g', 'y', 'e', 'g'), ('y', 'g', 'y', 'y', 'e'), ('y', 'g', 'y', 'y', 'y'), ('y', 'g', 'y', 'y', 'g'), ('y', 'g', 'y', 'g', 'e'), ('y', 'g', 'y', 'g', 'y'), ('y', 'g', 'y', 'g', 'g'), ('y', 'g', 'g', 'e', 'e'), ('y', 'g', 'g', 'e', 'y'), ('y', 'g', 'g', 'e', 'g'), ('y', 'g', 'g', 'y', 'e'), ('y', 'g', 'g', 'y', 'y'), ('y', 'g', 'g', 'y', 'g'), ('y', 'g', 'g', 'g', 'e'), ('y', 'g', 'g', 'g', 'y'), ('y', 'g', 'g', 'g', 'g'), ('g', 'e', 'e', 'e', 'e'), ('g', 'e', 'e', 'e', 'y'), ('g', 'e', 'e', 'e', 'g'), ('g', 'e', 'e', 'y', 'e'), ('g', 'e', 'e', 'y', 'y'), ('g', 'e', 'e', 'y', 'g'), ('g', 'e', 'e', 'g', 'e'), ('g', 'e', 'e', 'g', 'y'), ('g', 'e', 'e', 'g', 'g'), ('g', 'e', 'y', 'e', 'e'), ('g', 'e', 'y', 'e', 'y'), ('g', 'e', 'y', 'e', 'g'), ('g', 'e', 'y', 'y', 'e'), ('g', 'e', 'y', 'y', 'y'), ('g', 'e', 'y', 'y', 'g'), ('g', 'e', 'y', 'g', 'e'), ('g', 'e', 'y', 'g', 'y'), ('g', 'e', 'y', 'g', 'g'), ('g', 'e', 'g', 'e', 'e'), ('g', 'e', 'g', 'e', 'y'), ('g', 'e', 'g', 'e', 'g'), ('g', 'e', 'g', 'y', 'e'), ('g', 'e', 'g', 'y', 'y'), ('g', 'e', 'g', 'y', 'g'), ('g', 'e', 'g', 'g', 'e'), ('g', 'e', 'g', 'g', 'y'), ('g', 'e', 'g', 'g', 'g'), ('g', 'y', 'e', 'e', 'e'), ('g', 'y', 'e', 'e', 'y'), ('g', 'y', 'e', 'e', 'g'), ('g', 'y', 'e', 'y', 'e'), ('g', 'y', 'e', 'y', 'y'), ('g', 'y', 'e', 'y', 'g'), ('g', 'y', 'e', 'g', 'e'), ('g', 'y', 'e', 'g', 'y'), ('g', 'y', 'e', 'g', 'g'), ('g', 'y', 'y', 'e', 'e'), ('g', 'y', 'y', 'e', 'y'), ('g', 'y', 'y', 'e', 'g'), ('g', 'y', 'y', 'y', 'e'), ('g', 'y', 'y', 'y', 'y'), ('g', 'y', 'y', 'y', 'g'), ('g', 'y', 'y', 'g', 'e'), ('g', 'y', 'y', 'g', 'y'), ('g', 'y', 'y', 'g', 'g'), ('g', 'y', 'g', 'e', 'e'), ('g', 'y', 'g', 'e', 'y'), ('g', 'y', 'g', 'e', 'g'), ('g', 'y', 'g', 'y', 'e'), ('g', 'y', 'g', 'y', 'y'), ('g', 'y', 'g', 'y', 'g'), ('g', 'y', 'g', 'g', 'e'), ('g', 'y', 'g', 'g', 'y'), ('g', 'y', 'g', 'g', 'g'), ('g', 'g', 'e', 'e', 'e'), ('g', 'g', 'e', 'e', 'y'), ('g', 'g', 'e', 'e', 'g'), ('g', 'g', 'e', 'y', 'e'), ('g', 'g', 'e', 'y', 'y'), ('g', 'g', 'e', 'y', 'g'), ('g', 'g', 'e', 'g', 'e'), ('g', 'g', 'e', 'g', 'y'), ('g', 'g', 'e', 'g', 'g'), ('g', 'g', 'y', 'e', 'e'), ('g', 'g', 'y', 'e', 'y'), ('g', 'g', 'y', 'e', 'g'), ('g', 'g', 'y', 'y', 'e'), ('g', 'g', 'y', 'y', 'y'), ('g', 'g', 'y', 'y', 'g'), ('g', 'g', 'y', 'g', 'e'), ('g', 'g', 'y', 'g', 'y'), ('g', 'g', 'y', 'g', 'g'), ('g', 'g', 'g', 'e', 'e'), ('g', 'g', 'g', 'e', 'y'), ('g', 'g', 'g', 'e', 'g'), ('g', 'g', 'g', 'y', 'e'), ('g', 'g', 'g', 'y', 'y'), ('g', 'g', 'g', 'y', 'g'), ('g', 'g', 'g', 'g', 'e'), ('g', 'g', 'g', 'g', 'y'), ('g', 'g', 'g', 'g', 'g')]

WORDS = None
with open("Words/wordle-words.json") as words_json:
    WORDS = json.load(words_json)
WORDS = list(WORDS)

class Node():
    def __init__(self, new_id, new_value, new_depth, new_cost = 0, new_path = []):
        self.id = new_id
        self.value = new_value
        self.depth = new_depth
        self._child_nodes = []
        self.cost = new_cost
        self._path = copy.deepcopy(new_path)

    def add_node(self, new_node = None):
        if(new_node == None):
            self._child_nodes.append(Node())
        else:
            self._child_nodes.append(new_node)

    def get_node(self, index):
        return(self._child_nodes[index])

    def num_nodes(self):
        return(len(self._child_nodes))

    def add_to_path(self, id):
        self._path.append(id)

    def get_path(self):
        return(self._path)

    def prune(self):
        for i in list(self._child_nodes):
            if(i.cost <= 0):
                self._child_nodes.remove(i)


def build_node(node):
    if(node.depth < 12):
        for i in range(len(WORDS)):
            GLOBAL_ID_LOCK.acquire()
            node.add_node(Node(get_global_id(), WORDS[i], node.depth+1, new_path=node.get_path()))
            GLOBAL_ID_LOCK.release()
            new_node = node.get_node(i)
            for z in range(len(POSSIBLE_RESULT_ARRAY)):
                GLOBAL_ID_LOCK.acquire()
                new_node.add_node(Node(get_global_id(), POSSIBLE_RESULT_ARRAY[z], node.depth+1, new_path=node.get_path()))
                GLOBAL_ID_LOCK.release()
                build_node(new_node.get_node(z))

def build_tree():
    GLOBAL_ID_LOCK.acquire()
    head = Node(get_global_id(), "", 0)
    GLOBAL_ID_LOCK.release()
    build_node(head)


if __name__ == '__main__':
    build_tree()
