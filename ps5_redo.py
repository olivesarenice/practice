"""
You're building a tool for a currency trading desk.
The tool needs to be able to calculate the conversion path between any two currencies,
given a set of direct exchange rates (e.g., USD to EUR, EUR to GBP, etc.).
How would you write a program to solve this?
"""

# Clarify the requirements and input data:
# 1. the input is a pair of currencies --> (SGD, JPY) and the output is a single value (float) == conversion multiplier
# 2. data provided to me has ALL possible trading pairs and their respective exchange rates 


PAIRS = {
    "USD_GBP": 0.56,
    "GBP_USD": 1.3,
    "GBP_SGD": 1.8,
    "SGD_USD": 0.67,
    "SGD_JPY": 50,
    "USD_JPY":  70,
    "JPY_USD": 0.015
    } # forward and backwards may not be exactly equal ] 

# Problem: find the shortest (in terms of edges) path between 2 nodes (currencies).
# The multiplier is the product of all the edges along this path. Assume that we are not looking for the BEST rate, just the one with minimal conversions



from collections import defaultdict


def create_graph(pairs):
    dep_graph = defaultdict(list)
    for pair, rate in pairs.items():
        from_cur = pair.split("_")[0]
        to_cur = pair.split("_")[1]
        dep_graph[to_cur].append(from_cur)
    print(dep_graph)
    return dep_graph

# BFS starting from our start node.
from collections import deque


def form_pairs_path(path):
    conversion_path = [c for c in reversed(path)]
    pairs = []
    for i, item in enumerate(conversion_path):
        if i == 0:
            continue
        pair = f"{conversion_path[i-1]}_{conversion_path[i]}"
        pairs.append(pair)
    return pairs

def traverse(from_cur, to_cur,dep_graph):
    
    seen = set(to_cur)
    queue = deque([(to_cur,[to_cur])]) # stores (start_node, path_to_start_node)
    while queue:
        node, path_to_node = queue.popleft()
        
        for child in dep_graph[node]:
            if child not in seen:
                # visit the child
                new_path = path_to_node + [child]
                if child == from_cur:
                    print(new_path)
                    return form_pairs_path(new_path)
                else:
                    seen.add(child)
                    queue.append((child, new_path))
    return None
        

def get_multiplier(valid_path, pairs):
    rate = 1
    for i, pair in enumerate(valid_path):
        if i == 0:
            continue
        rate *= pairs[pair]
    return rate
    

from_cur = "GBP"
to_cur = "JPY"

# expected: GBP --> SGD --> JPY => rate = 1.8*50 
valid_path = traverse(from_cur, to_cur, create_graph(PAIRS))
if valid_path:
    print(valid_path)
    rate = get_multiplier(valid_path, PAIRS)
    print(rate)


"""
The real value of this tool would be in automatically spotting profit opportunities. 
An 'arbitrage' is a cycle of trades that results in a net profit. 
How could your program analyze the exchange rates to detect if any such opportunities exist?
"""

# 1. calculate all possible paths that result in a cycle starting from A -> A
# 2. pick the cycle that has the largest value > 1 ($1 of A will give $1+ of A)

def find_cycle(currency,dep_graph):
    from collections import Counter

    #seen = set(to_cur)
    seen = Counter({currency:1})
    queue = deque([(currency,[currency])]) # stores (start_node, path_to_start_node)
    cycles = []
    print(dep_graph[currency])
    while queue:
        print(queue)
        node, path_to_node = queue.popleft()
        print(node)
        
        for child in dep_graph[node]:
            # if (child not in path_to_node):
            if seen.get(child, 0) <= 1: # we allow at most 1 cycle (i.e. to walk back on itself eventually)
                # visit the child
                new_path = path_to_node + [child]
                if child == currency:
                    cycles.append(form_pairs_path(new_path))
                else:
                    seen_counter = seen.get(child,0)
                    seen[child] = seen_counter +1
                    queue.append((child, new_path))
    return cycles


cycle_registry = {} # {id: (cycle_path, arb_value)}
cycles = find_cycle("SGD", create_graph(PAIRS))
for i, cycle in enumerate(cycles):
    rate = get_multiplier(cycle, PAIRS)
    cycle_registry[i] = (cycle, rate)

print(cycle_registry)
# lets say we are looking for arb in SGDs, anytime any rate changes, need to calc all paths for SGD again
# 1. store a reverse index, each arb cyclic path has N different currencies
# SGD_JPY : [path1, path2, path3...] (SGD appears in these paths)
# GBP_USD : [path2, path3 ...] 
# if GBP_USD changes, we only recalculate p2, p3, but NOT p1 --> we know that this change doesnt affect the arb of p1./
# if the new p2/ p3 are more $$$ the top arb of the list, then we can replace it instantly, otherwise, no need to check anything else.

def create_curr_path_index(cycle_registry):
    inverse_map = defaultdict(list)
    
    # first recreate the pairs:
    for id, cycle in cycle_registry.items():
        for pair in cycle[0]:
            inverse_map[pair].append(id)
    return inverse_map

inv_map = create_curr_path_index(cycle_registry)
for m in inv_map:
    print("------")
    print(m)
    print("::")
    print(inv_map[m])
    
changed = ("JPY_USD", 75)
def update_cycle_registry(pair, rate, cycle_registry, inv_map):
    affected_cycles = inv_map.get(pair, [])
    print("AFFECTED:")
    print(affected_cycles)
    for id in affected_cycles:
        PAIRS.update({pair:rate})
        new_rate = get_multiplier(cycle, PAIRS)
        print(new_rate)
        cycle_registry[id] = (cycle, new_rate)
        
    print("UPDATE:")
    print(cycle_registry)


update_cycle_registry(changed[0], changed[1], cycle_registry, inv_map)