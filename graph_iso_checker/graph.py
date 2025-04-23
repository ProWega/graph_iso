import random
import json


class Graph:
    def __init__(self, num_vertices):
        # инициализация пустого неориентированного графа
        self.num_vertices = num_vertices
        self.adj = {i: set() for i in range(num_vertices)}


    def add_edge(self, u, v):
        # добавить ребро (без петель)
        if u == v:
            return
        self.adj[u].add(v)
        self.adj[v].add(u)


    def has_edge(self, u, v):
        # проверка, есть ли ребро u–v
        return v in self.adj.get(u, ())


    def neighbors(self, u):
        # возвращает множество соседей вершины u
        return self.adj[u]


    def random_permutation(self):
        # возвращает изоморфный граф и саму перестановку вершин
        perm = list(range(self.num_vertices))
        random.shuffle(perm)
        g2 = Graph(self.num_vertices)
        for u in range(self.num_vertices):
            for v in self.adj[u]:
                if u < v:
                    g2.add_edge(perm[u], perm[v])
        return g2, perm


    def to_json(self):
        # сериализация в JSON
        data = {
            'num_vertices': self.num_vertices,
            'adjacency': [sorted(self.adj[u]) for u in range(self.num_vertices)]
        }
        return json.dumps(data)


    @classmethod
    def from_json(cls, s):
        # десериализация из JSON
        data = json.loads(s)
        g = cls(data['num_vertices'])
        for u, nbrs in enumerate(data['adjacency']):
            for v in nbrs:
                g.add_edge(u, v)
        return g


def generate_random_graph(n, p):
    # генерация случайного графа G(n, p)
    g = Graph(n)
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                g.add_edge(u, v)
    return g




