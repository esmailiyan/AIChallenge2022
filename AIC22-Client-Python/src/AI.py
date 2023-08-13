import random
from src.client import GameClient
from src.model import GameView

def get_thief_starting_node(view: GameView) -> int:
    id = view.viewer.id
    graph = Graph(view.config.graph.paths, view.config.graph.nodes)
    nodes = graph.nodes
    nodes.sort(key=lambda x: graph.degree[x], reverse=True)
    id = id%5
    return nodes[id]

class Utils:
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

class Phone:
    def __init__(self, client: GameClient):
        self.client = client

    def send_message(self, message):
        self.client.send_message(message)

class AI:
    def __init__(self, view: GameView, phone: Phone):
        self.phone = phone
        self.graph = Graph(view.config.graph.paths, view.config.graph.nodes)
        self.mark = []
        self.thief_nodes = []

    def thief_move_ai(self, view: GameView) -> int:
        id = view.viewer.id
        team = view.viewer.team
        type = view.viewer.agent_type
        is_dead = view.viewer.is_dead
        balance = view.balance
        status = view.status
        node_id = view.viewer.node_id
        turn_id = view.turn.turn_number
        chat_box = view.chat_box
        visible_agents = view.visible_agents
        visible_turns = view.config.visible_turns

        adj = self.graph.adj
        node = self.graph.nodes
        degree = self.graph.degree

        try:
            police_nodes = []
            filter = {"team": not team, "type": not type, "dead": is_dead}
            for agent in visible_agents:
                check = {"team": agent.team, "type": agent.agent_type, "dead": agent.is_dead}
                if filter == check:
                    police_nodes.append(agent.node_id)
            print(f"turn:{turn_id:<3}, thief:{id:<4}, SUCCESS FIELD 1 , police_nodes:{str(police_nodes)}")
        except:
            print(f"turn:{turn_id:<3}, thief:{id:<4}, ERROR FIELD 1")

        try:
            dangerousـnodes = []
            for p in police_nodes:
                for (u, w) in adj[p]:
                    if u not in dangerousـnodes and u not in police_nodes:
                        dangerousـnodes.append(u)
            dangerousـnodes.sort(key=lambda x: -degree[x])
            print(f"turn:{turn_id:<3}, thief:{id:<4}, SUCCESS FIELD 2 , dangerousـnodes:{str(dangerousـnodes)}")
        except:
            print(f"turn:{turn_id:<3}, thief:{id:<4}, ERROR FIELD 2")

        try:
            riskyـnodes = []
            for d in dangerousـnodes:
                for (u, w) in adj[d]:
                    if u not in riskyـnodes and u not in dangerousـnodes and u not in police_nodes:
                        riskyـnodes.append(u)
            riskyـnodes.sort(key=lambda x: -degree[x])
            print(f"turn:{turn_id:<3}, thief:{id:<4}, SUCCESS FIELD 3 , riskyـnodes:{str(riskyـnodes)}")
        except:
            print(f"turn:{turn_id:<3}, thief:{id:<4}, ERROR FIELD 3")

        try:
            safe_nodes = []
            for (u, w) in adj[node_id]:
                if u not in riskyـnodes and u not in dangerousـnodes and u not in police_nodes:
                    safe_nodes.append(u)
            safe_nodes.sort(key=lambda x: -degree[x])
            print(f"turn:{turn_id:<3}, thief:{id:<4}, SUCCESS FIELD 4 , safe_nodes:{str(safe_nodes)}")
        except:
            print(f"turn:{turn_id:<3}, thief:{id:<4}, ERROR FIELD 4")

        try:
            neighbors = []
            for (u, w) in adj[node_id]:
                neighbors.append(u)
            print(f"turn:{turn_id:<3}, thief:{id:<4}, SUCCESS FIELD 5 , neighbors:{str(neighbors)}")
        except:
            print(f"turn:{turn_id:<3}, thief:{id:<4}, ERROR FIELD 5")

        try:
            prices = {}
            for (u, w) in adj[node_id]:
                prices[u] = w
            print(f"turn:{turn_id:<3}, thief:{id:<4}, SUCCESS FIELD 6 , prices:{str(prices)}")
        except:
            print(f"turn:{turn_id:<3}, thief:{id:<4}, ERROR FIELD 6")

        try:
            for s in safe_nodes:
                if prices[s] <= balance:
                    return s
            for r in riskyـnodes:
                if r in neighbors and prices[r] <= balance:
                    return r
            for d in dangerousـnodes:
                if d in neighbors and prices[d] <= balance:
                    return d
            return node_id
        except:
            print(f"turn:{turn_id:<3}, thief:{id:<4}, ERROR FIELD 6")
            return node_id

    def police_move_ai(self, view: GameView) -> int:
        id = view.viewer.id
        team = view.viewer.team
        type = view.viewer.agent_type
        is_dead = view.viewer.is_dead
        balance = view.balance
        status = view.status
        node_id = view.viewer.node_id
        turn_id = view.turn.turn_number
        chat_box = view.chat_box
        visible_agents = view.visible_agents
        visible_turns = view.config.visible_turns

        adj = self.graph.adj
        node = self.graph.nodes
        degree = self.graph.degree

        try:
            if turn_id in visible_turns:     
                self.mark = [node_id]
                self.thief_nodes = []
                filter = (not team, not type, is_dead)
                for agent in visible_agents:
                    check = (agent.team, agent.agent_type, agent.is_dead)
                    if filter == check:
                        self.thief_nodes.append(agent.node_id)
            print(f"turn:{turn_id:<3}, police:{id:<3}, SUCCESS FIELD 1 , thief_nodes:{str(self.thief_nodes)}")
        except:
            print(f"turn:{turn_id:<3}, police:{id:<3}, ERROR FIELD 1")

        try:
            partners = []
            filter = (team, type, is_dead)
            for agent in visible_agents:
                check = (agent.team, agent.agent_type, agent.is_dead)
                if filter == check:
                    if agent.node_id not in self.mark:
                        self.mark.append(agent.node_id)
                    partners.append(agent.node_id)
            print(f"turn:{turn_id:<3}, police:{id:<3}, SUCCESS FIELD 2 , partners:{str(partners)}")
        except:
            print(f"turn:{turn_id:<3}, police:{id:<3}, ERROR FIELD 2")

        try:
            options = []
            for thief in self.thief_nodes:
                path = self.graph.find_path(start=node_id, target=thief)
                if path not in options:
                    options.append(path)
            print(f"turn:{turn_id:<3}, police:{id:<3}, SUCCESS FIELD 3 , options:{str(options)}")
        except:
            print(f"turn:{turn_id:<3}, police:{id:<3}, ERROR FIELD 3")

        try:
            enemys = []
            for o in options:
                if len(o) == len(options[0]):
                    enemys.append(o[-1])
            print(f"turn:{turn_id:<3}, police:{id:<3}, SUCCESS FIELD 4 , enemys:{str(enemys)}")
        except:
            print(f"turn:{turn_id:<3}, police:{id:<3}, ERROR FIELD 4")

        try:
            neighbors = []
            for (u, w) in adj[node_id]:
                neighbors.append(u)
            print(f"turn:{turn_id:<3}, police:{id:<3}, SUCCESS FIELD 5 , neighbors:{str(neighbors)}")
        except:
            print(f"turn:{turn_id:<3}, police:{id:<3}, ERROR FIELD 5")

        try:
            moves = []
            for n in neighbors:
                for e in enemys:
                    path = self.graph.find_path(start=n, target=e, without=node_id)
                    if path not in moves and node_id not in path:
                        moves.append(path)
            moves.sort(key=lambda x: len(x))
            print(f"turn:{turn_id:<3}, police:{id:<3}, SUCCESS FIELD 6 , moves:{str(moves)}")
        except:
            print(f"turn:{turn_id:<3}, police:{id:<3}, ERROR FIELD 6")

        try:
            prices = {}
            for (u, w) in adj[node_id]:
                prices[u] = w
            print(f"turn:{turn_id:<3}, thief:{id:<4}, SUCCESS FIELD 7 , prices:{str(prices)}")
        except:
            print(f"turn:{turn_id:<3}, thief:{id:<4}, ERROR FIELD 7")

        try:
            for m in moves:
                if m[0] not in self.mark and prices[m[0]] <= balance:
                    return m[0]
            random.shuffle(neighbors)
            for n in neighbors:
                if prices[n] <= balance:
                    return n
        except:
            print(f"turn:{turn_id:<3}, police:{id:<3}, ERROR FIELD 8")
            return node_id
