from collections import defaultdict
import pprint
from timeit import default_timer as timer

class Graph():

    '''Graph Class -> Can be directed or undirected(default)
                   -> Can be weighted or unweighted(default)
                   -> Can have a heuristic or not(default)'''

    def __init__(self, edgelist, directed=False, weighted=False, heuristic=False):

        '''
        Initialize graph using a list of edges.
        If Unweighted-> edgelist=(Node 1, Node2)
        If Weighted-> edgelist=(Node 1, Node2, Edge Weight)

        :param edgelist: Node to start search from
        :param directed: Set if graph is directed or undirected (default=Flase) 
        :param weighted: Set if graph is weighted or unweighted (default=Flase)
        :param heuristic: Set if graph requires a heuristic or not (default=Flase)

        :return: None 
        '''

        self.adj = defaultdict(set)
        self.directed = directed
        self.weighted = weighted
        self._initialize(edgelist) # fill out adjacency list
        if heuristic:
            self.heuristic = {}
            self.generate_heuristics() # Generate heuristic f option is set

    def _initialize(self,edgelist):
        
        if not self.weighted: # unweighted edges
            for source,dest in edgelist:
                self.add(source,dest)
        else:
            for source,dest,weight in edgelist: # weighted edges
                self.add(source,dest,weight)

    def add(self,node1,node2,weight=None):

        '''
        Function used to add edges to the graph.
        
        :param node1: Node to start search from
        :param node2: Node to search for
        :param weight: Weights of the edge for weighted Graphs (defaut=None)

        :return: None 
        '''

        if weight is None:
            self.adj[node1].add(node2)
            if not self.directed: # addedge from a-b to b-a also if graph is undirected
                self.adj[node2].add(node1)
        else:
            self.adj[node1].add((node2,weight)) # add pairs node1 : (node2,weight)
            if not self.directed: 
                self.adj[node2].add((node2,weight))


    def generate_heuristics(self):
        # Can be modified to generate heuristic, but we will use a hard coded one  for now
        self.heuristic = {1: 5, 2: 7, 3: 3, 4: 4, 5: 6, 6: 5, 7: 6, 8: 0, 9: 0, 10: 0}

    def bfs(self, start, target):

        '''
        Breath First Search where given a source and target node using breath
        first method we attempt to find the path to target node.
        
        :param start: Node to start search from
        :param target: Node to search for

        :return: Path to node if found 
        '''

        visited=set()
        q=[]
        traversal=[] # remember path taken
        visited.add(start)
        q.append(start)
        while q:
            node=q.pop(0)
            traversal.append(node)
            if node==target: # stop when goal node is reached
                return traversal
            for other in self.adj[node]: # for every neighbour if not visited add to queue and mark visited
                if other not in visited:
                    visited.add(other)
                    q.append(other)
        return "Node not Found"
        
    def dfs(self, start, target):

        '''
        Deapth First Search where given a source and target node using depth
        first method we attempt to find the path to target node.
        
        :param start: Node to start search from
        :param target: Node to search for

        :return: Path to node if found 
        '''

        result=[]
        visited=set()
        self._helper_dfs(start,visited,result,target)
        if target in result:
            return result
        else:
            return"Node not Found"

    def _helper_dfs(self, node, visited, result, target):
        if result and result[-1]==target: # if goal node is visited then returns 
            return
        visited.add(node)
        result.append(node)
        
        for other in self.adj[node]: # for every neighbour if not visited run dfs on it
            if other not in visited:
                self._helper_dfs(other,visited,result,target)

    def dls(self, start, target, max_depth):

        '''
        Deapth Limited Search where given a maximum depth path will be
        returned only if node is found at or before the maximum depth.

        :param start: Node to start search from
        :param target: Node to search for
        :param max_depth: Maximum depth to limit search space <= maximum depth

        :return: Path to node if found 
        '''

        result=[]
        visited=set()
        depth=defaultdict()
        depth[start]=0
        self._helper_dls(start,visited,result,target,depth,max_depth)
        if target in result:
            return result
        else:
            return"Node not Found"

    def _helper_dls(self, node, visited, result, target, depth, max_depth):

        if depth[node]>max_depth: # check maximum depth condition
            return
        if result and result[-1]==target: # check if goal node is found
            return
        visited.add(node)
        result.append(node)
        for other in self.adj[node]:
            if other not in visited:
                depth[other]=depth[node]+1 # keeps track of depth ->depth of child is parent+1
                self._helper_dls(other,visited,result,target,depth,max_depth)

    def iterative_deepening(self, start, target, max_depth):

        '''
        Iterative Deepening Search where given a maximum depth we will search
        iteratively in every depth from 0-max_depth and return path if found.

        :param start: Node to start search from
        :param target: Node to search for
        :param max_depth: Maximum depth to limit search space <= maximum depth

        :return: Path to node if found 
        '''

        flag=0
        for current_depth in range(max_depth+1): # for every depth from 0 to maximum depth run a depth limited search
            result=self.dls(start,target,current_depth)
            if not isinstance(result,str):
                return result
        return "Node not Found"
            
    def bi_directional(self):
        pass

    def Astar(self,start, target):
        result = set()
        visited = set()
        pqueue = []
        star= defaultdict()
        star[start]= 0
        target_found =False
        self._helper_Astar(star, visited, start, target, pqueue, result, target_found)
        if target in result:
            return result
        else:
            return"Node not Found"

    def _helper_Astar(self, star, visited, node, target, pqueue, result, target_found):
        if target_found:
            return
        visited.add(node)
        result.add(node)
        for other in self.adj[node]:
            if other in visited:
                continue
            visited.add(other)
            pqueue.append(other)
            if target == other[0]:
                target_found = True
                return

        while len(pqueue)!=0:
            x = min(pqueue)[1]
            for i in range(len(pqueue)):
                if pqueue[i][1]== x:
                    x=i
                    break
            if pqueue[x] in result: result.pop(pqueue[x])
            node2 = pqueue.pop(x)
            # if node2 in visited: continue
            self._helper_Astar(star, visited, node2[0], target, pqueue, result, target_found)


    def __str__(self):
        return f'{dict(self.adj)}'



'''
    2
   /  
  7 -- 10
 / \  
1    6 --    5
 \    \
  8    11
   \
    9
     \
      4
'''

edgelist = [(1,7),(7,2),(7,10),(7,6),(6,5),(6,11),(1,8),(8,9),(9,4)]

# https://media.cheggcdn.com/media/cb6/cb6e15aa-4815-47a4-b2ff-ca9086722f40/phpj6mHyD
# s1  a2  b3  c4  d5  e6  f7  g1 8  g2 9  g3 10

# edgelist=[(1,2,5),(1,3,9),(1,5,6),(2,3,3),(2,8,9),(3,2,2),(3,4,2),(4,1,6),(4,7,7),(4,9,5),(5,1,1),(5,4,1),(5,6,2),(6,10,7),(7,5,2),(7,10,8),(8,9,0)]
# graph=Graph(edgelist, True, True, True)

graph=Graph(edgelist)
printer=pprint.PrettyPrinter()
printer.pprint(dict(graph.adj))
# print(graph)

'''
start = timer()

bfs=graph.bfs('A','K')

end = timer()
print(end - start)
print(bfs)
'''

print('\nPath Algorithm takes until it reaches target: \nBreath First Search (BFS)')
print(graph.bfs(1,4))

print('\nPath Algorithm takes until it reaches target: \nDepth First Search (DFS)')
print(graph.dfs(1,4))

print('\nPath Algorithm takes until it reaches target: \nDepth Limit Search (DLS)')
print(graph.dls(1,11, 4))

print('\nPath Algorithm takes until it reaches target: \nIterative Deepening (IDDFS)')
print(graph.iterative_deepening(1,11, 4))

# print('\nPath Algorithm takes until it reaches target: \nA-star (A*)')
# print(graph.Astar(1,10))


