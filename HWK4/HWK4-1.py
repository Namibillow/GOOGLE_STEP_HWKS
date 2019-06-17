class Vertex:
    def __init__(self, id):
        self.id = id
        self.neighbors = []
        self.visited = False
        self.prev = None
        self.dist = 0

    def addNeighbor(self, neigh):
        self.neighbors.append(neigh)

    def __str__(self):
        return str(self.id) + ' is connected to ' + str([n.id for n in self.neighbors])

    def getConnections(self):
        return self.neighbors

    def getVertexInfo(self):
        return self.id


class Graph:
    def __init__(self):
        self.verticies = {}
        self.numVerticies = 0

    def addVertex(self, id):
        self.numVerticies += 1
        newV = Vertex(id)
        self.verticies[id] = newV

    def addEdge(self, from_id, to_id):
        if from_id not in self.verticies.keys():
            self.addVertex(from_id)
        if to_id not in self.verticies.keys():
            self.addVertex(to_id)
        self.verticies[from_id].addNeighbor(self.verticies[to_id])


def bfs(graph, start, goal):

    for vertex in graph.verticies.values():
        vertex.visited = False
        vertex.dist = 0
        vertex.prev = None

    queue = [start]
    start.visited = True

    while queue:
        vertex = queue.pop(0)
        for neighbor in graph.verticies[vertex.id].neighbors:
            if not neighbor.visited:
                neighbor.visited = True
                neighbor.dist = vertex.dist + 1
                neighbor.prev = vertex
                queue.append(neighbor)
                if neighbor == goal:
                    return True
    return False


def print_bfs(graph, start_id, goal_id, names):

    start = graph.verticies[start_id]
    goal = graph.verticies[goal_id]

    if not bfs(graph, start, goal):
        print("Not connected")
        return

    path = [names[goal.id]]
    previous = goal
    while previous.prev:
        path.append(names[previous.prev.id])
        previous = previous.prev

    print(f"Shortest path length is : {goal.dist}")

    print(f"Shortest path is : ")
    print(path[::-1])


def build_graph(file_path):
    with open(file_path, 'r') as f:
        graph = Graph()
        for line in f.readlines():
            from_vertex, to_vertex = map(int, line.split())
            graph.addEdge(from_vertex, to_vertex)
        return graph


def read_names(file_path):
    '''
    build a dictionary where key is id and value is name
    '''
    with open(file_path, 'r') as f:
        names = {}
        for line in f.readlines():
            id, name = line.split()
            names[int(id)] = name
        return names


if __name__ == '__main__':
    names = read_names('nicknames.txt')

    graph = build_graph('links.txt')

    start, goal = map(int, input('Type two numbers between 0 to 48 separate by comma: ').split())
    print_bfs(graph, start, goal, names)


# clone this repo
# go to directory HWK4/
# run command: pyhton3 HWK4-1.py
# will ask you to input 2 numbers separating by a space
# will return output
