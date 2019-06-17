import argparse

# Google 457783


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


def build_graph(file_path):
    with open(file_path, 'r') as f:
        graph = Graph()
        for line in f.readlines():
            from_vertex, to_vertex = map(int, line.split())
            graph.addEdge(from_vertex, to_vertex)
        return graph


def read_wiki(file_path):
    '''
    build a dictionary where key is id and value is wiki title
    '''
    with open(file_path, 'r') as f:
        titles = {}
        for line in f.readlines():
            id, title = line.split()
            titles[int(id)] = title
        return titles


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process search queary")
    parser.add_argument('-s --source', required=True, type=str, help="Search term to start", default="Google")
    parser.add_argument('--dest', required=True, type=str, help="Destination you would like to find a connection")
    parser.add_argument('--dest2', type=str, help="2nd Destination you want to find")

    parser.add_argument('--compare', action='store_true')  # compares two terms
    parser.add_argument('--shortest', action='store_true')  # find shortest paths
    parser.add_argument('__all_paths')
    args = parser.parse_args()

    wiki_titles = read_wiki('wikipedia_links/pages.txt')

    graph = build_graph('wikipedia_links/links.txt')
