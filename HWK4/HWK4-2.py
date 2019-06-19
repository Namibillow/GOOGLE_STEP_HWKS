import argparse

from HWK4_1 import print_bfs, Graph

# Google 457783


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
        reverse_title = {}
        for line in f.readlines():
            id, title = line.split()
            titles[int(id)] = title
            reverse_title[title] = int(id)
        return titles, reverse_title


def print_dfs(graph, start_id, goal_id, titles):

    start = graph.verticies[start_id]
    goal = graph.verticies[goal_id]

    for vertex in graph.verticies.values():
        vertex.visited = False
        vertex.dist = 0
        vertex.prev = None

    path = []

    dfs(graph, start, goal, path)


def dfs(graph, s, d, path):
    path.append(s)
    s.visited = True

    if s == d:
        print(path)
    else:
        for neighbor in s.neighbors:
            if not neighbor.visited:
                dfs(graph, neighbor, d, path)

    path.pop()
    s.visited = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process search queary")
    parser.add_argument('-s', '--source', required=True, type=str, help="Search term to start", default="Google")
    parser.add_argument('--dest', required=True, type=str, help="Destination you would like to find a connection")
    # parser.add_argument('--dest2', type=str, help="2nd Destination you want to find")

    parser.add_argument('--cycle', action='store_true')  # compares two terms
    parser.add_argument('--shortest', action='store_true')  # find shortest paths
    parser.add_argument('--all_paths', action='store_true')
    args = parser.parse_args()

    wiki_titles, reverse_wiki_titles = read_wiki('wikipedia_links/pages.txt')

    try:
        source = reverse_wiki_titles[args.source]
        dest = reverse_wiki_titles[args.dest]
    except:
        print("NOT A VALID INPUT")

    graph = build_graph('wikipedia_links/links.txt')

    print("GRAPH IS READY TO BE EXPLORED!")

    if args.all_paths:
        print_dfs(graph, source, dest, wiki_titles)
    elif args.shortest:
        print_bfs(graph, source, dest, wiki_titles)
    elif args.cycle:
        # print_cycle()
        pass
