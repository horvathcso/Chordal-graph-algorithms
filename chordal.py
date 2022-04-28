import networkx as nx
from random import randint,choice
from itertools import combinations

def LexBFS(G):
    nodes=set(G.nodes)
    i=len(nodes)
    ls_sets=[nodes]
    ls_sets=list(filter(lambda x: x!=set(), ls_sets))
    order={n:None for n in nodes}
    while len(ls_sets)>0:
        p=ls_sets[0].pop()
        i-=1
        order[p]=i
        N=set(G.neighbors(p))
        ls_splited=[]
        for S in ls_sets:
            ls_splited.append(S.intersection(N))
            ls_splited.append(S-N)
        ls_sets=list(filter(lambda x: x!=set(), ls_splited))
    return order


def is_chordal(G):
        """Checks whether G is a chordal graph.

        A graph is chordal if every cycle of length at least 4 has a chord
        (an edge joining two nodes not adjacent in the cycle).

        Parameters
        ----------
        G : graph
          A NetworkX graph. (Should not be digraph or multigraph)

        Returns
        -------
        chordal : bool
          True if G is a chordal graph and False otherwise.

        Notes
        -----
        Based on the algorithms in [1]_. 
        Iterate the following from P={V}.
        P = {P1, P2, . . . , Pk}, and a pivot p from P1, append p to the order. 
        We use N(p) to refine P by creating the following new partition
        {P1 ∩ N(p), P1-N(p), P2 ∩ N(p), P2-N(p), . . . , Pi ∩ N(p), Pi-N(p), . . . , Pk ∩ N(p), Pk-N(p)}, 
        while maintaining the order of the partition classes and leav the empy ones out. 
        The algorithm stops when all the partition classes are either empty.

        References
        ----------
        .. [1] Michel Habib, Ross McConnell, Christophe Paul, and Laurent Viennot. 
        Lex-bfs and partition refinement, with applications to transitive orientation, 
        interval graph recognition and consecutive ones testing.
        Theoretical Computer Science, 234(1):59–84, 2000.
        """
    order=LexBFS(G)
    dic_Np={n:set() for n in G.nodes}
    dic_last={n:None for n in G.nodes}
    for i,j in G.edges:
        if order[i]<order[j]:
            dic_Np[i].add(j)
            if dic_last[i]==None:
                dic_last[i]=j
            elif order[j]<order[dic_last[i]]:
                dic_last[i]=j
        else: 
            dic_Np[j].add(i)
            if dic_last[j]==None:
                dic_last[j]=i
            elif order[i]<order[dic_last[j]]:
                dic_last[j]=i
    for n in sorted(order, key=order.get):
        p=dic_last[n]
        if not p==None:
            if not (dic_Np[n]-{p}).issubset(dic_Np[p]):
                return False
    return True


    



def coloring(G):
    """
        Gives an eficient algorithm for the coloring problem in chordal graphs
    
    """
    def N_p(G,n, oreder, col):
        """
            The color of the greater neighbors of n in the G networkx graph respect to the order.
        """
        greater_col=set()
        i=oreder.index(n)
        for j in range(len(oreder)-1,i,-1):
            if G.has_edge(n,oreder[j]):
                greater_col.add(col[order[j]])
        return greater_col
    
    if not is_chordal(G):
        raise ValueError("The given graph is not chordal")
    
    order=LexBFS(G)
    col={k:None for k in order}
    #col[len(order)-1]=1
    for e in reversed(order):
        greater_col=N_p(G,e,order,col) 
        for i in range(0,len(greater_col)+1):
            if not i in greater_col:
                col[e]=i
    return col    