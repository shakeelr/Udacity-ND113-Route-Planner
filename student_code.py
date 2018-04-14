from math import sqrt

def distance(a,b):
#helper function to find the straight line distance between two points on the map
    x = b[0]-a[0]
    y = b[1]-a[1]
    return sqrt(x*x + y*y)

def shortest_path(M,start,goal):
    
    #initialize sets for the frontier and explored space
    frontier = set([start])
    explored = set()
 
    #create a dict to keep track of paths, and intialize it with the start path
    #Note: I needed to keep track of paths in a seperate list, as lists and dictionary are 
    #      not hashable.  However, the size of the list is kept small by only keeping track
    #      of paths in the frontier.
    start_path = {
            "node" : start,
            "coordinates" : M.intersections[start],
            "parent" : False,
            "g" : 0,
            "cost" : distance(M.intersections[start], M.intersections[goal])
    }
    paths = {start : start_path}
    
    #loop
    while frontier:
        #find the cheapest path in the frontier
        cheapest_node = next(iter(frontier))
        for node in frontier:
            if paths[node]["cost"] < paths[cheapest_node]["cost"]:
                cheapest_node = node
        cheapest_path = paths[cheapest_node]
            

        #explore the cheapest path
        #get the set of roads that connect to intersection corresponding to the cheapest path excluding the explored set
        roads = set(M.roads[cheapest_path["node"]]) - explored

        #update frontier and explored sets
        frontier = frontier.union(roads)
        explored.add(cheapest_path["node"])
        frontier.remove(cheapest_path["node"])

        #update paths
        for node in roads:
            
            #some parameters used to update paths
            parent = cheapest_path["node"]
            #calculate cost using the straight line distance as my huristic
            g = cheapest_path["g"] + distance(M.intersections[node], M.intersections[cheapest_path["node"]]) 
            h = distance(M.intersections[node], M.intersections[goal])
            f = g + h
            
            #if there is already a path to a node, only update it if the new path is cheaper
            if node not in paths or f < paths[node]["cost"]:
                paths[node] = {
                    "node" : node,
                    "coordinates" : M.intersections[node],
                    "parent": parent,
                    "g" : g,
                    "cost" : f 
                }
        
        #if the cheapest path is the goal return it's actions
        if cheapest_path["node"] == goal:
            actions = [goal]
            node = goal
            while paths[node]["parent"]:
                actions.insert(0,paths[node]["parent"])
                node = paths[node]["parent"]
            return actions
        
    
    #if the frontier is empty, return error
    return "No path to goal found"
    
    print("cheapest path called")
    return