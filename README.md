#**Assessment: Undirect Graph, Connected Components and Resilience of Computer Networks**  
    
Write Python code that implements breadth-first search. Then, you will use this function to compute the set of connected components (CCs) of an undirected graph as well as determine the size of its largest connected component. You will write a function that computes the resilience of a graph (measured by the size of its largest connected component) as a sequence of nodes are deleted from the graph. Then we will analyze the connectivity of a computer network as it undergoes a cyber-attack. In particular, we will simulate an attack on this network in which an increasing number of servers are disabled. In computational terms, we will model the network by an undirected graph and repeatedly delete nodes from this graph. We will then measure the resilience of the graph in terms of the size of the largest remaining connected component as a function of the number of nodes deleted.  
- Computer network : load the file as an undirected graph (with 1239 nodes and 3047 edges)
  http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt
- ER graphs
- UPA graphs  
First,examine the resilience of the computer network under an attack in which servers are chosen at random. We will then compare the resilience of the network to the resilience of ER and UPA graphs of similar size. Once you have computed the resilience for all three graphs, plot the results as three curves combined in a single standard plot (not log/log). Use a line plot for each curve. The horizontal axis for your single plot be the the number of nodes removed (ranging from zero to the number of nodes in the graph) while the vertical axis should be the size of the largest connect component in the graphs resulting from the node removal.
We will say that a graph is resilient under this type of attack if the size of its largest connected component is roughly (within ~25%) equal to the number of nodes remaining, after the removal of each node during the attack. Which of the three graphs are resilient under random attacks as the first 20% of their nodes are removed?    

The function *targeted_order* takes an undirected graph ugraph and iteratively does the following:
    Computes a node of the maximum degree in ugraph. If multiple nodes have the maximum degree, it chooses any of them (arbitrarily).
    Removes that node (and its incident edges) from ugraph.    

Implement *fast_targeted_order* method, creating a list degree_sets whose k-th element is the set of nodes of degree k, the method then iterates through the list degree_sets in order of decreasing degree. When it encounter a non-empty set, the nodes in this set must be of maximum degree. The method then repeatedly chooses a node from this set, deletes that node from the graph, and updates degree_sets appropriately.  
Analyze the running time of these two methods on UPA graphs of size nnn with m=5.   
Compute a plot comparing the running times of these methods on UPA graphs of increasing size.  

Next, run these two functions on a sequence of UPA graphs with n in range(10, 1000, 10) and m=5 and use the time module (or your favorite Python timing utility) to compute the running times of these functions. Then, plot these running times (vertical axis) as a function of the number of nodes n (horizontal axis) using a standard plot (not log/log). What are tight upper bounds on the worst-case running times of targeted_order and fast_targeted_order? Use big-O notation to express your answers.  

Using targeted_order (or fast_targeted_order), your task is to compute a targeted attack order for each of the three graphs (computer network, ER, UPA). Then, for each of these three graphs, compute the resilience of the graph using compute_resilience. Finally, plot the computed resiliences as three curves (line plots) in a single standard plot.   

Now, consider removing a significant fraction of the nodes in each graph using targeted_order. Examine the shape of the three curves from your plot in above question. Which of the three graphs are resilient under targeted attacks as the first 20% of their nodes are removed? Again, note that there is no need to compare the three curves against each other in your answer to this question.  


#**Outcomes:**  

- Analyzing the plots of the three graphs under random attack we can see that if the first 20% of their nodes removed, all of them are resilient. The three have linear negative slop with the rise of the number of nodes.  
- The big-O notations of targeted_order anf fast_targeted_order functions are  O(n^2) and O(n+m) repectively (m - number of edges), which correspond to the shapes of their running times: quadratic and linear.  
- The computer network is not resilient at all under targeted order attacks, that is removing the node of the biggest degree and its edges at every attack. After removing 20% of it's first  nodes the sizes of the biggest connected components fall to nearly zero. ER and UPA graphs are resilient to the targeted attacks but would these methods be taken to consideration in buiding the computer neworks despite the high cost of their realizations due to the enormous geographical logistic issues of creating of such servers?  

