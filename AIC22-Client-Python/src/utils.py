def log(data: str) -> bool:
    addr = "/home/mahdi/Documents/AIC22-Client-Python/log.txt"
    try: 
        with open(addr, "a") as file:
            file.write(data + '\n')   
        return True
    except:
        return False

class Message:
    def decode_msg(msg: str) -> int:
        try:
            data = int(msg, base=2)
            return data
        except:
            print(f"Error in decode_msg! -> msg={msg}")
    def encode_msg(msg: int) -> str:
        try:
            data = format(msg, "b")
            return data
        except:
            print(f"Error in encode_msg! -> msg={msg}")

class Graph:
    def __init__(self, Edges, Nodes):
        '''----- config structures -----'''
        self.adj = {}
        self.degree = {}
        self.nodes = []
        self.edges = []
        '''----- handle nodes -----'''
        for N in Nodes:
            self.nodes.append(N.id)
        '''----- handle nodes -----'''
        for E in Edges:
            self.edges.append((E.first_node_id, E.second_node_id, E.price))
        '''----- handle data -----'''
        for v in self.nodes:
            self.adj[v] = []
        '''----- config graph -----'''
        for (v, u, w) in self.edges:
            self.adj[v].append((u, w))
            self.adj[u].append((v, w))
        '''----- config degree -----'''
        for v in self.nodes:
            self.degree[v] = len(self.adj[v])
        '''----- sort edges -----'''
        for v in self.nodes:
            self.adj[v].sort(key=lambda e: [e[1], -self.degree[e[0]]])

    def find_path(self, start: int, target: int, without=0, prices=[0, 25, 50]):
        '''----- config structures -----'''
        list = []
        mark = {}
        parent = {}
        '''----- config data -----'''
        for v in self.nodes:
            mark[v] = False
            parent[v] = -1
        '''----- config setup -----'''
        list.append(start)
        mark[start] = True
        parent[start] = 0
        '''----- start bfs -----'''
        for v in list:
            for (u, w) in self.adj[v]:
                if not mark[u] and w in prices and u != without:
                    mark[u] = True
                    parent[u] = v
                    list.append(u)
        '''----- find path -----'''
        ans = []
        pt = target
        while pt > 0:
            ans.append(pt)
            pt = parent[pt]
        ans.reverse()
        return ans

    def find_dist(self, start: int, target: int, prices=[0, 25, 50]):
        path = self.find_path(start=start, target=target, prices=prices)
        return len(path)-1
