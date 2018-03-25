import numpy as np
import random, time, copy, gc


def read_input():
    global edge_dic
    def one_edge():
        global edge_dic
        line = input()
        u, v, w = line.split()
        edge_dic[(int(u), int(v))] = float(w)
        return int(u), int(v), float(w)
    n = int(input())
    edges = [one_edge() for _ in range(4 * n**2 - 2*n)]
    return n, edges


def weight_of_edge(i, j):
    global edge_dic
    return edge_dic[(i, j)]


def state2graph(state):
    # input: state
    # output: graph for this state
    global edges
    n = len(state)
    graph = np.zeros((n+1, n+1), dtype=np.float64)
    for u, v, w in edges:
        if (u == 0 or u in state) and v in state:
            graph[abs(u), abs(v)] = w
    return graph

def power_from_graph(graph):
    # input: graph
    # output: power for this graph
    n = len(graph)-1
    mat_l = np.zeros((n+1, n+1), dtype=np.float64)
    for i in range(n+1):
        for j in range(n+1):
            if i == j:
                for k in range(n+1):
                    if k != i:
                        mat_l[i, j] += graph[k, i]
            else:
                mat_l[i, j] = -graph[i, j]
    det = np.linalg.det(mat_l[1:, 1:])
    del mat_l
    junk = gc.collect()
    return det



def augment_graph(old_graph, old_states, new_state):
    n = len(old_graph) - 1
    new_graph = np.zeros((n+2, n+2), dtype=np.float64)
    new_graph[0:n+1, 0:n+1] = old_graph
    del old_graph
    junk = gc.collect()
    for i in range(0, n+2):
        try:
            if i == 0:
                new_graph[0, abs(new_state)] = weight_of_edge(0, new_state)
            else:
                new_graph[i, abs(new_state)] = weight_of_edge(old_states[i-1], new_state)
        except:
            pass
    for i in range(0, n+2):
        try:
            if i == 0:
                new_graph[abs(new_state), 0] = weight_of_edge(new_state, 0)
            else:
                new_graph[abs(new_state), i] = weight_of_edge(new_state, old_states[i-1])
        except:
            pass
    return new_graph



def dp(current_determined_states, current_determined_graph, max_iter):
    global counter
    if counter >= max_iter:
        return current_determined_states, current_determined_graph
    k = len(current_determined_states)
    new_state_1 = current_determined_states + [k+1]
    new_graph_1 = augment_graph(current_determined_graph, current_determined_states, k+1)
    new_power_1 = power_from_graph(new_graph_1)
    new_state_2 = current_determined_states + [-(k+1)]
    new_graph_2 = augment_graph(current_determined_graph, current_determined_states, -(k+1))
    new_power_2 = power_from_graph(new_graph_2)
    if new_power_1 > new_power_2:
        next_determined_states = new_state_1
        next_determined_graph = new_graph_1
        del new_state_2, new_graph_2, new_power_2
    else:
        next_determined_states = new_state_2
        next_determined_graph = new_graph_2
        del new_state_1, new_graph_1, new_power_1
    junk = gc.collect()
    counter += 1
    return dp(next_determined_states, next_determined_graph, max_iter)





def change_state_graph(n, current_state, current_graph, j):
    # this set of states include a useless 0
    # j \in [1, ..., n]
    global edge_dic
    next_graph = copy.deepcopy(current_graph)
    for i in range(0, n+1):
        if i != j:
            try:
                next_graph[i, j] = weight_of_edge(i, j)
            except:
                pass
    for i in range(0, n+1):
        if i != j:
            try:
                next_graph[j, i] = weight_of_edge(j, i)
            except:
                pass
    next_state = copy.deepcopy(current_state)
    try:
        next_state[j] = -next_state[j]
    except:
        pass
    return next_state, next_graph





def iter_single(state, graph):
    n = len(state)
    current_power = power_from_graph(graph)
    for i in range(1, n+1):
        next_state, next_graph = change_state_graph(n, state, graph, i)
        next_power = power_from_graph(next_graph)
        if next_power > current_power:
            return iter_single(next_state, next_graph)
    return state, graph



global n, edge_dic

edge_dic = {}
n, edges = read_input()

gc.enable()

for u, v, w in edges:
    edge_dic[(u, v)] = w

global initial_states, counter
initial_states = [1, 2]
counter = len(initial_states)
initial_graph = state2graph(initial_states)





states_A, graph_A = dp(initial_states, initial_graph, 500)
states_B, graph_B = dp(states_A, graph_A, 800)
states_C, graph_C = dp(states_B, graph_B, 1100)
states_D, graph_D = dp(states_C, graph_C, 1200)
states_E, graph_E = dp(states_D, graph_D, 1300)
states_F, graph_F = dp(states_E, graph_E, 1400)
states_G, graph_G = dp(states_F, graph_F, n)
print (' '.join('%+d' % i for i in states_G))
