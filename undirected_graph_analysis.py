"""
Write Python code that implements breadth-first search. Then, you will use this function to compute the set of
connected components (CCs) of an undirected graph as well as determine the size of its largest connected component.
Finally, you will write a function that computes the resilience of a graph (measured by the size
 of its largest connected component) as a sequence of nodes are deleted from the graph.
Then we will analyze the connectivity of a computer network as it undergoes a cyber-attack. In particular, we will simulate
an attack on this network in which an increasing number of servers are disabled.  In computational terms, we will model
the network by an undirected graph and repeatedly delete nodes from this graph. We will then measure the resilience of
the graph in terms of the size of the largest remaining connected component as a function of the number of nodes deleted.
- Computer network : load the file as an undirected graph (with 1239 nodes and 3047 edges)
  http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt
- ER graphs
_ UPA graphs


"""
import random
import upa_class
import urllib.request as urllib2
from collections import deque
from timeit import default_timer as timer
import matplotlib.pyplot as plt
UPA_URL = "http://www.codeskulptor.org/#alg_upa_trial.py"
NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph ugraph and the node start_node and
    returns the set consisting of all nodes that are visited by a breadth-first search that starts at start_node.
    :param ugraph:
    :param start_node:
    :return:
    """
    queue = deque()
    visited = set()
    if start_node not in ugraph.keys():
        return None
    visited.add(start_node)
    queue.append(start_node)
    while len(queue) > 0:
        node = queue.popleft()
        for neighbor in list(ugraph[node]):
            if not neighbor in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited

def cc_visited(ugraph):
    """
    Takes the undirected graph ugraph and returns a list of sets, where each set consists of all the nodes
    (and nothing else) in a connected component, and there is exactly one set in the list for each connected component
    in ugraph and nothing else.
    :param ugraph:
    :return:
    """
    cc_nodes = []
    remain_nodes = list(ugraph.keys())
    while remain_nodes:
        node_i = remain_nodes[0]
        cc_node = bfs_visited(ugraph, node_i)
        cc_nodes.append(cc_node)
        remain_nodes_copy = list(remain_nodes)
        for dummy in cc_node:
            if dummy in remain_nodes_copy:
                remain_nodes.remove(dummy)
    return cc_nodes

def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph and returns the size (an integer) of the largest connected component in ugraph.
    :param ugraph:
    :return:
    """
    sizes_list = []
    if cc_visited(ugraph) == []:
        return 0
    for component in cc_visited(ugraph):
        sizes_list.append(len(component))

    return max(sizes_list)

#Graph resilience
def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph ugraph, a list of nodes attack_order and iterates through the nodes in attack_order.
    For each node in the list, the function removes the given node and its edges from the graph and then computes
    the size of the largest connected component for the resulting graph. The function should return a list whose k+1 th
    entry is the size of the largest connected component in the graph after the removal of the first k nodes in attack_order.
    The first entry (indexed by zero) is the size of the largest connected component in the original graph.
    """
    ugraph_copy = copy_graph(ugraph)
    resilience = [largest_cc_size(ugraph)]
    for node in attack_order:
        neighbors = ugraph_copy[node]
        for neighbor in neighbors:
            if node in ugraph[neighbor]:
                ugraph_copy[neighbor].remove(node)
        del ugraph_copy[node]
        resilience.append(largest_cc_size(ugraph_copy))
    return resilience[:-1]

#Analysis of a Computer Network

def er_graph(num_nodes, p):
    """
    Create a random undirected graph
    """
    ugraph = {}
    set_nodes = [set() for dummy_x in range(num_nodes)]
    for num_x in range(num_nodes):
        for num_y in range(num_x + 1, num_nodes):
            if random.random() <= p:
                set_nodes[num_x].add(num_y)
                set_nodes[num_y].add(num_x)
    for dummy in range(num_nodes):
        ugraph[dummy] = set_nodes[dummy]
    return ugraph

def read_graph(data_url):
    """

    :param file_url:
    :return:
    """
    file_data = urllib2.urlopen(data_url)
    file_data = file_data.read()
    file_data = file_data.decode()
    file_data = file_data.split("\n")
    file_data = file_data[:-1]
    print("Loaded graph with ",len(file_data),"nodes")
    answer_graph = {}
    for line in file_data:
        line = line.split()
        node = int(line[0])
        set_nodes = set([])
        for neighbor in line[1:]:
            set_nodes.add(int(neighbor))
        answer_graph[node] = set_nodes
    return answer_graph

def random_order(ugraph):
    """
    takes a graph and returns a list of the nodes in the graph in some random order.
    """
    attack_list = list(ugraph.keys())
    random.shuffle(attack_list)
    return attack_list

def upa_graph(num_nodes, m):
    """
    Generate a random undirected graph num_nodes, m (m≤n), which is the number of existing nodes to which a new node is
    connected during each iteration. Notice that m is fixed throughout the procedure. Then, the algorithm grows the
    graph by adding n−m nodes, where each new node is connected to m nodes randomly chosen from the set of existing nodes.
    As an existing node may be chosen more than once in an iteration, we eliminate duplicates (to avoid parallel edges);
    hence, the new node may be connected to fewer than m existing nodes upon its addition.
    """
    upa_graph = er_graph(m, 1)
    set_nodes = upa_class.UPATrial(m)
    for idx in range(m, num_nodes):
        value = set_nodes.run_trial(m)
        upa_graph[idx] = value
        for node in value:
            upa_graph[node].add(idx)
    return upa_graph

#network undirected graph (with 1239 nodes and 3047 edges)
def edges_number(ugraph):
    """
    """
    num = 0
    for node in list(ugraph.keys()):
        num += len(ugraph[node])
    return int(num/2.)

def build_plot(ugraph1, ugraph2, ugraph3, flag):
    """
    Plot the results as three curves combined in a single standard plot (not log/log). Use a line plot for each curve.
    The horizontal axis for your single plot be the the number of nodes removed (ranging from zero to the number of
    nodes in the graph) while the vertical axis should be the size of the largest connect component in the graphs resulting from the node removal.
    """
    if flag == 1:
        attack_order1 = random_order(ugraph1)
        attack_order2 = random_order(ugraph2)
        attack_order3 = random_order(ugraph3)
        plt.title("The resilence of the Network, ER and UPA graphs on random attack order")

    elif flag == 2:
        attack_order1 = targeted_order(ugraph1)
        attack_order2 = targeted_order(ugraph2)
        attack_order3 = targeted_order(ugraph3)
        plt.title("The resilence of the Network, ER and UPA graphs on targeted attack order")
    else:
        attack_order1 = fast_targeted_order(ugraph1)
        attack_order2 = fast_targeted_order(ugraph2)
        attack_order3 = fast_targeted_order(ugraph3)
        plt.title("The resilence of the Network, ER and UPA graphs on fast targeted attack order")

    resilience_list1 = compute_resilience(ugraph1, attack_order1)
    resilience_list2 = compute_resilience(ugraph2, attack_order2)
    resilience_list3 = compute_resilience(ugraph3, attack_order3)
    plt.plot(range(len(attack_order1)), resilience_list1)
    plt.plot(range(len(attack_order2)), resilience_list2)
    plt.plot(range(len(attack_order3)), resilience_list3)
    plt.xlabel("Number of removed nodes")
    plt.ylabel("Resilience")
    # plt.title("The resilence of the Network, ER and UPA graphs on random attack order")
    plt.legend(["Network graph 1239 nodes", "ER graph n = 1239, p = 0.004", "UPA graph n =1239, m = 3"])
    plt.show()

def copy_graph(ugraph):
    """
    copy graph
    :param ugraph:
    :return:
    """
    new_graph = {}
    for node in ugraph:
        new_graph[node] = set(ugraph[node])
    return new_graph

def targeted_order(ugraph):
    """
    Computes a node of the maximum degree in ugraph. If multiple nodes have the maximum degree, it chooses any of them (arbitrarily).
    Removes that node (and its incident edges) from ugraph.
    Observe that targeted_order continuously updates ugraph and always computes a node of
    maximum degree with respect to this updated graph
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)
        order.append(max_degree_node)
    return order

def compute_degree(ugraph, node):
    """
    return the degree of the node
    """
    if ugraph[node] == set():
        return 0
    return len(ugraph[node])

def fast_targeted_order(ugraph):
    """
    This method creates a list degree_sets whose k-th element is the set of nodes of degree k.
    The method then iterates through the list degree_sets in order of decreasing degree.
    When it encounter a non-empty set, the nodes in this set must be of maximum degree.
    The method then repeatedly chooses a node from this set, deletes that node from the graph,
    and updates degree_sets appropriately.
    """
    ugraph_new = copy_graph(ugraph)
    degree_sets = {}
    #degree_sets[k] is a set of all nodes whose degree is k
    for dummy in range(len(ugraph)):
        degree_sets[dummy] = set([])
    for dummy_node in ugraph:
        degree = compute_degree(ugraph, dummy_node)
        degree_sets[degree].add(dummy_node)

    #initiatial an empty list
    nodes_list = []
    idx = 0
    for idx_k in range(len(ugraph) - 1, 0, -1):
        # remove from k_degree list all the neighbors of node_u and add them to one k-1 degree list
        if not degree_sets[idx_k]:
            continue
        while degree_sets[idx_k]:
            node_u = list(degree_sets[idx_k])[0]
            neighbors = ugraph[node_u]
            degree_sets[idx_k].remove(node_u)
            if not neighbors:
                degree_sets[0].add(node_u)
            for neighbor in neighbors:
                degree_nei = compute_degree(ugraph, neighbor)
                if neighbor in degree_sets[degree_nei]:
                    degree_sets[degree_nei].remove(neighbor)
                    degree_sets[degree_nei - 1].add(neighbor)
            nodes_list.append(node_u)
            idx += 1
            #delete node_u from the ugraph
            neighbors_set = ugraph_new[node_u]
            for dummy in neighbors_set:
                if node_u in ugraph_new[dummy]:
                     ugraph_new[dummy].remove(node_u)
            del ugraph_new[node_u]
    for node in ugraph.keys():
        if not node in nodes_list:
            nodes_list.append(node)
    return nodes_list

def running_time(m):
    """
    Run these  targeted_order and fast_targeted_order functions on a sequence of UPA graphs with n in range(10, 1000, 10) and m=5 and
    use the time module (or your favorite Python timing utility) to compute the running times of these functions.
    Then, plot these running times (vertical axis) as a function of the number of nodes n (horizontal axis) using a
    standard plot (not log/log).
    """
    fast_target_run = []
    target_run =[]
    for num_nodes in range(10, 1000, 10):
        ugraph = upa_graph(num_nodes, m)
        start = timer()
        targeted_order(ugraph)
        end = timer()
        target_run.append((end - start))
        start = timer()
        fast_targeted_order(ugraph)
        end = timer()
        fast_target_run.append((end - start))
    plt.plot(range(10, 1000, 10),target_run )
    plt.plot(range(10, 1000, 10), fast_target_run)
    plt.xlabel("number of nodes")
    plt.ylabel("running time")
    plt.title(" Running time of Targeted Order and Fast Targeted Order functions ")
    plt.legend(["Targeted Order", "Fast Targeted Order"])
    plt.show()

ugraph1 = read_graph(NETWORK_URL )
num_nodes = 1239
m = 5
p = .004
ugraph2 = er_graph(num_nodes, p)
ugraph3 = upa_graph(num_nodes, m)
# flag = 3
# build_plot(ugraph1, ugraph2, ugraph3, flag)
running_time(m)