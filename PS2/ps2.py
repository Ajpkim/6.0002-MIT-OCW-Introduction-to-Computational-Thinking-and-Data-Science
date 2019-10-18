# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
# The nodes represent the buildings and the edges represent paths connecting buildings. The distances
# between the buildings (nodes) are represented by the weighted edges which contain information about the 
# total distance between nodes as well as the outdoors distance between the nodes

# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    
    print("Loading map from file...")

#   Create a new graph
    graph = Digraph()

#   Read in the data from the file
    with open(map_filename, 'r') as map_data:        

        for line in map_data:
            
        # Split the line by '' to isolate the 4 variables of interest                    
            line_data = line.split()
            
            src = Node(line_data[0])
            dest = Node(line_data[1])
            
            total_distance = int(line_data[2])
            outdoor_distance = int(line_data[3])
            
        # Create a weighted edge from src to dest             
            new_wedge = WeightedEdge(src, dest, total_distance, outdoor_distance)
        
        #If src or dest nodes not graph, then create them            
            if not graph.has_node(src):
                graph.add_node(src)
            
            if not graph.has_node(dest):
                graph.add_node(dest)
        
#           Add the new edge to the grapg        
            graph.edges[src].append(new_wedge)
        
    return graph
            
            

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

#map_filename = 'test_load_map.txt'
#
#
#test_graph = (load_map(map_filename))
#
#print (test_graph)
##Not sure why the close parenthese is printing on next line 
## --> bc I wasn't importing distances as ints
#
#print ('Here are the nodes in the test graph:', test_graph.nodes)
#print ('')
#for node in test_graph.nodes:
#    print ('Node', node, 'is the source of', len(test_graph.edges[node]), 'edges')
#
#print ('')
#edge_count = 0
#for edge in test_graph.edges.values():
#    edge_count += 1
#print (edge_count)



#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?

# Answer:
# The objective function is to minimize travel distance by finding path between nodes that 
# has the lowest distance 

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """

#    create node instances from given start and end strings    
    start_node = Node(start)
    end_node = Node(end)
    

#   If start or end node not in graph, raise ValueError       
    if not (digraph.has_node(start_node) and digraph.has_node(end_node)):
        raise ValueError('Node not in graph')
        
#   Recursive base case: if the start and end node are the same, then return the associated path and total distance with case
#                           (meaning the path and distance that led up to this call... the associated path)
    elif start == end:
        # update global vars
        return path[0], path[1]
        
#    Recursive case
    else:

#        Check all the edges from current start node
            
        for edge in digraph.edges[start_node]:    
#           Setting explicit variables for readability... going to use in creating new test path used to check the current edge

#           This is going to get added to the test path list of strings, meaning I need a STRING which is why there's a call to the get_name method of the node
            new_node = edge.get_destination().get_name()
#            Creating test path nodes by adding new node to the path list 
            test_path_nodes = path[0] + [new_node]
#            Create the new distances by updating path distances with current edge distance
            new_total_path_distance = path[1] + edge.get_total_distance()
            new_outdoor_path_distance = path[2] + edge.get_outdoor_distance()
        
        
#           Create new path that includes the current edge being explored
            test_path = [test_path_nodes, new_total_path_distance, new_outdoor_path_distance]


#           Check all constraints to see if edge is worth exploring
#            Have we already been to the edge destination in path? Is path longer than best solution so far? Is path over outdoors limit?
            if (new_node not in path[0]) and (test_path[1] < best_dist) and (test_path[2] <= max_dist_outdoors): 
                
#            If test_path meets all constraints, then explore it, and find recursive solution for the path
                follow_edge = get_best_path(digraph, new_node, end, test_path, max_dist_outdoors, best_dist, best_path)

#               if a solution is found and that solution is shorter than the best distance found so far we will update global variables
                if follow_edge != None and follow_edge[1] < best_dist:
                    
#                    Set best distance to total distance of current solution
                    best_dist = follow_edge[1]
#                    Set the best path to the current test path
                    best_path = follow_edge[0]
        
#        If there is an existing solution, meaning best path is NOT empty
        if best_path:
#            return tuple of the best path and the total distance of that path
            return best_path, best_dist
        
#        else, no solution has been found and return None 
        else: 
            return None
                
        
        
        

        
# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
#    
#    Call get_best_path with given args/constraints and store result
    result = get_best_path(digraph, start, end, [[start], 0, 0], max_dist_outdoors, float('inf'), [])
    
#    If result is None or the total distance of path exceeds given constraint, raise ValueError
    if result == None or result[1] > max_total_dist:
        raise ValueError('No possible path')
        
#    Otherwise, return the best path portion of result (leaving out the associated total distance)
    else: 
        return result[0]
    
    

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
