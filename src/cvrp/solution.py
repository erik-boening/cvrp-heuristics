def solution_cost(routes, dist):
    allcost = 0
    for r in routes:
        allcost += route_cost(r, dist)
    return allcost

def route_cost(route, dist):
    cost = dist[0, route[0]]
    length = len(route)
    for i in range(1, length):
        cost += dist[route[i-1], route[i]]
    cost += dist[route[-1], 0]
    return cost

def route_load(route, demand):
    allDemand = 0
    length = len(route)
    for i in range(1, length):
        allDemand += demand[route[i]]
    return allDemand

def is_feasible(routes, demand, capacity):
    visited = []
    for r in routes:
        if(len(r)==0):
            return False
        for customer in r:
            if customer < 1 or customer >= len(demand):
                return False
        if(route_load(r, demand)>capacity):
            return False
        visited = visited+r
    if(sorted(visited) != list(range(1, len(demand)))):
        return False
    return True