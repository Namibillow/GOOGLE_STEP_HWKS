class Vertex:
    def __init__(self, id):
        self.id = id
        self.neighbors = []

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
        self.verticies[id] = Vertex(id)

    def addEdge(self, from_id, to_id):
        if from_id not in self.verticies.keys():
            self.addVertex(from_id)
        if to_id not in self.verticies.keys():
            self.addVertex(to_id)
        self.verticies[from_id].addNeighbor(self.verticies[to_id])


def bfs(graph, start, goal):
    """
    Return:
        A boolean value True meaning it has a path
    """
    is_visited = [False] * graph.numVerticies
    dist = [0] * graph.numVerticies
    prev = [None] * graph.numVerticies

    queue = [start]
    is_visited[start.id] = True

    while queue:
        vertex = queue.pop(0)
        for neighbor in graph.verticies[vertex.id].neighbors:
            if not is_visited[neighbor.id]:
                id = neighbor.id
                is_visited[id] = True
                dist[id] = dist[vertex.id] + 1
                prev[id] = vertex.id
                queue.append(neighbor)
                if neighbor == goal:
                    return prev, dist
    return None, None


def print_bfs(graph, start_id, goal_id, names):

    start = graph.verticies[start_id]
    goal = graph.verticies[goal_id]
    path, dist = bfs(graph, start, goal)
    if path:
        temp = goal_id
        shortest_path = [names[goal_id]]
        while path[temp]:
            shortest_path.append(names[path[temp]])
            temp = path[temp]

        print(f"{dist[goal_id]} shortest path steps.")

        print(f"Shortest path is : ", end=" ")
        print(shortest_path[::-1])
    else:
        print("Oupsy Not connected!!")


def build_graph(file_path, name_list):
    """
    build a graph and add edges
    """

    with open(file_path, 'r') as f:
        graph = Graph()

        for name_id in name_list.keys():
            graph.addVertex(name_id)

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
        names_rev = {}
        for line in f.readlines():
            id, name = line.split()
            names[int(id)] = name
            names_rev[name] = int(id)
        return names, names_rev


NAMES_FILE = 'nicknames.txt'
LINKS_FILE = 'links.txt'

if __name__ == '__main__':
    names, names_reversed = read_names(NAMES_FILE)

    graph = build_graph(LINKS_FILE, names)

    start, goal = input('Type 2 names separate by a space: ').lower().split()

    try:
        start, goal = names_reversed[start], names_reversed[goal]
    except:
        print("invalid names")

    print_bfs(graph, start, goal, names)
