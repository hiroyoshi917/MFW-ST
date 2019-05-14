#
# constructor of SuffixTrie
# (2019/05/04)
# (2019/05/13)

# the final step
import numpy as np
import copy
from graphviz import Digraph


class SuffixTrie(Digraph):
    """
    A data structure to represent a binary suffix trie
    """
    def __init__(self, text):
        self.nNodes = 0
        self.nEdges =  0
        self.trie = []
        self.parent = []
        self.degree = []
        self.forks = []
        self.G = Digraph(format='png')
        self.G.attr('node', shape='circle')
        self.text = text
        self.suffixes = self.sortedSuffixes()
        self.build(text)

    def node(self, str1, str2):
        self.G.node(str1, str2)
        self.nNodes += 1

    def edge(self, str1, str2):
        self.G.edge(str1, str2)

    def edgeC(self, str1, str2, opt):
        self.G.edge(str1, str2, color=opt)
        self.nEdges += 1

    def edgeLC(self, str1, str2, optL, optC):
        self.G.edge(str1, str2, label=optL, color=optC)
        self.nEdges += 1

    def view(self):
        self.G.view()

    def getSuffixes(self, text):
        return [text[i:] for i in range(len(text))]
    #
    def sortedSuffixes(self):
        lsuff = [self.text[i:] for i in range(len(self.text))]
        lsuff.sort()
        return lsuff
    #
    def calcLCP(self, s, t):
        l = min(len(s), len(t))
        m = 0
        for i in range(l):
            if (s[i] == t[i]):
                m += 1
            else:
                break
        return m
    #
    def getLCP(self, ss):
        aLCP=[]
        for i in range(len(ss)):
            if (i == 0):
                aLCP.append(-1)
            else:
                aLCP.append(self.calcLCP(ss[i-1], ss[i]))
        return aLCP


    def firstPathV3(self, s, len_nextstr):
       # making nodes for string s including the root node
        self.degree.append(0)
        self.trie.append({})
        for i in range(1, len(s)+1):
            if (i == len(s) and len(s) > len_nextstr):
#                self.G.attr('node', shape='square')
                self.G.node(str(i), str(i), shape='square')
#                self.G.attr('node', shape='circle')
            else:
                self.G.node(str(i), str(i))
            #
            self.nNodes += 1
            self.degree.append(0)
            self.trie.append({})

        # making edges
        for i in range(len(s)):
            self.G.edge(str(i), str(i+1), label=str(s[i]))
            self.nEdges += 1
            self.degree[i] += 1
            self.trie[i].setdefault(s[i], i+1)

        # house keeping
        return [len(s)+1, range(len(s)+1)]

    def nextPathV3(self, s, lcpv, len_nextstr, nextID, prevPath):
        # making nodes for string s
#        print("nextPath: lcpv, len(s) ", lcpv, len(s))
        for i in range(lcpv, len(s)):
            if (i == len(s)-1 and len(s) != len_nextstr):
                self.G.node(str(nextID+i-lcpv), str(nextID+i-lcpv), shape='square')
            else:
                self.G.node(str(nextID+i-lcpv), str(nextID+i-lcpv))
#        nodeID.append(nextID+i-lcpv)
            self.nNodes += 1
            self.degree.append(0)
            self.trie.append({})

        # making edges for string s
        for i in range(nextID, nextID+len(s)-lcpv):
            if (i == nextID):
                prev = prevPath[lcpv]
            else:
                prev = i-1
            self.G.edge(str(prev), str(i), label=s[i-nextID+lcpv])
            self.nEdges += 1
            self.degree[prev] += 1
#        print("prev: ", prev)
            self.trie[prev].setdefault(s[i-nextID+lcpv], i)

        # house keeping
        #print("nextPath: ", lcpv)
        curPath = []
        for i in range(lcpv+1):
            curPath.append(prevPath[i])
        for i in range(lcpv, len(s)):
            curPath.append(int(nextID+i-lcpv))
        return[nextID+len(s)-lcpv, curPath]

    def getParents(self):
        p=[-1]*len(self.trie);
        for i in range(len(self.trie)):
            if '0' in self.trie[i]:
                p[self.trie[i]['0']] = i
            if '1' in self.trie[i]:
                p[self.trie[i]['1']] = i
        self.parent = copy.copy(p)

    def build(self, src):
        aSuf =  self.getSuffixes(src)
        aSuf.sort()                 # suffixes must be sorted
        aLCP = self.getLCP(aSuf)
        aLCP.append(0)        # add a sentinel

    # draw the first path
    # why do we need aLCP[1]?  For what?
    # because the first path may overlap with the next one. If it does so,
    # it does not have the leaf.  Instead of that, it will be fully covered by
    # the next path.
        [nextID, prevPath] = self.firstPathV3(aSuf[0], aLCP[1])

    #  print(prevPath)
    # draw other paths
        for i in range(1, len(aSuf)):
            [nextID, prevPath] = self.nextPathV3(aSuf[i], aLCP[i], aLCP[i+1], nextID,  prevPath)

    # get  list of forks
        self.forks = list(filter(lambda i: self.degree[i]>1, range(len(self.degree))))
        for i in range(len(self.forks)):
            self.G.node(str(self.forks[i]), color = 'red')
  #          self.nNodes += 1
    # get list of parents
        self.getParents()

    def info(self):
        print("nNodes: {0}\tnEdges: {1}".format(self.nNodes, self.nEdges))
        print("trie:\n", self.trie)
        print("parents:\n", self.parent)
        print("degree:\n", self.degree)
        print("forks:\n", self.forks)

    def locusL(self, pathL):
        cnode = 0
        for i in range(len(pathL)):

#            print("cnode at locusL: ", i, cnode)

            if pathL[i] in self.trie[cnode]:
                cnode = self.trie[cnode][pathL[i]]
            else:
                return -1
        return cnode

    def locusQ(self, pathL):
        if self.locusL(pathL) == -1:
            return False
        else:
            return True

    def path(self, node):
        pathstr = []
        if (node < len(self.trie)):
            cn = node
        else:
            return ''
        while cn != -1:
            pn = cn
            cn = self.parent[cn]
            if '0' in self.trie[cn] and self.trie[cn]['0'] == pn:
                pathstr.append('0')
            elif '1' in self.trie[cn] and self.trie[cn]['1'] == pn:
                pathstr.append('1')
        pathstr.reverse()
        return pathstr

    def leafQ(self, id):
         return len(self.trie[id]) == 0

#
#
#
# the final step

def createMFW(nt, pnode, node):
    '''
    create an MFW or MFWs to nt.
    '''
    t = nt.trie
    pList = nt.parent
    n = nt.nNodes

#     print("in createMFW, pnode: {0}\tnode: {1}".format(pnode, node))

    pathstr = nt.path(node)
    nt.G.attr('node', shape = 'doublecircle')

    if '0' not in t[node] and '0' in t[pnode]:
        print("MFW: ", pathstr+ ['0'])
        n += 1

#        print('in createMFW, n: ', n)

        nt.G.edge(str(node), str(n), label='0', style='bold', color='blue')
        t.append({})
        t[node]['0'] = n
        nt.parent.append(node)

    if  '1' not in t[node] and '1' in t[pnode]:
        print("MFW: ", pathstr+['1'] )
        n += 1

#        print('in createMFW, n: ', n)

        nt.G.edge(str(node), str(n), label='1', style='bold', color='blue')
        t.append({})
        t[node]['1'] = n
        nt.parent.append(node)

    nt.G.attr('node', shape = 'circle')
    nt.nNodes = n

def showMFWCandidates(st):
    s = copy.deepcopy(st)
    t = s.trie
    n = len(t)
    for i in range(len(t)):
        if not '0' in t[i]:
            s.G.edge(str(i), str(n), label="0", color='blue')
            n += 1
        if not '1' in t[i]:
            s.G.edge(str(i), str(n),  label="1", color='blue')
            n += 1
    s.G.view()

def buildADT(st):
    nt = copy.deepcopy(st)
    t = nt.trie
    parent = nt.parent
    forks = nt.forks
    flagLeaf = False


    # build MFWs of type L
    leaves=list(filter(lambda i: len(st.trie[i]) == 0, range(len(st.trie))))
    argmin=np.argmin([len(st.path(k)) for k in leaves])
    node_I = leaves[argmin]
    pathmin = st.path(node_I)
    pathmin = pathmin[1:]
    node_p = st.locusL(pathmin)

    nt.G.edge(str(node_p), str(node_I), color = 'green')
    nt.nEdges += 1
    createMFW(nt, node_p, node_I)

    # build MFWs of type I
    pathForks = [st.path(i) for i in forks]

#    print("pathForks: ", pathForks)

    for i in range(len(pathForks)):
        path0 = ['0']+pathForks[i]
        path1 = ['1']+pathForks[i]
        if st.locusQ(path0):
            node0 = st.locusL(path0)
            nt.G.edge(str(forks[i]), str(node0), color = 'green')
            nt.nEdges += 1

#            print("node0[{0}]: {1}".format(node0, nt.trie[node0]))

            createMFW(nt, forks[i], node0)

        if nt.locusQ(path1):
            node1 = st.locusL(path1)
            nt.G.edge(str(forks[i]), str(node1), color = 'green')
            nt.nEdges += 1

#            print("node1[{0}]: {1}".format(node1, nt.trie[node1]))

            createMFW(nt, forks[i], node1)

    return nt

def buildADT_FH(st):
    nt = copy.deepcopy(st)
    t = nt.trie
    parent = nt.parent
    forks = nt.forks
    flagLeaf = False

#    print('nt.info()')
#    nt.info()

    # build MFWs of type I
    pathForks = [nt.path(i) for i in forks]

#    print("pathForks: ", pathForks)

    for i in range(len(pathForks)):
        path0 = ['0']+pathForks[i]
        path1 = ['1']+pathForks[i]
        if nt.locusQ(path0):
            node0 = nt.locusL(path0)
            nt.G.edge(str(forks[i]), str(node0), color = 'green')
            nt.nEdges += 1

#            print("node0[{0}]: {1}".format(node0, nt.trie[node0]))

            if len(nt.trie[node0]) == 0:
                flagLeaf = True

#            createMFW(st, nt, forks[i], node0)

        if nt.locusQ(path1):
            node1 = nt.locusL(path1)
            nt.G.edge(str(forks[i]), str(node1), color = 'green')
            nt.nEdges += 1

#            print("node1[{0}]: {1}".format(node1, nt.trie[node1]))

            if len(nt.trie[node1]) == 0:
                flagLeaf = True

 #           createMFW(st, nt, forks[i], node1)

    # build MFWs of type L
    if flagLeaf == True:
#        print('skip to look for MFWs of type L')
        return nt
#    else:
#        print('continue to look for MFWs of type L')

    leaves=list(filter(lambda i: len(st.trie[i]) == 0, range(len(st.trie))))
    argmin=np.argmin([len(st.path(k)) for k in leaves])
    node_I = leaves[argmin]
    pathmin = st.path(node_I)
    pathmin = pathmin[1:]
    node_p = st.locusL(pathmin)

    nt.G.edge(str(node_p), str(node_I), color = 'green')
    nt.nEdges += 1
#    createMFW(st, nt, node_p, node_I)

    return nt

def buildADT_SH(at, st):
    '''
    complete AD trie from suffix trie st with MF links
    '''
 #   nt = copy.deepcopy(at)
    t = at.trie
    parent = at.parent
    forks = at.forks

    # build MFWs of type L

    leaves=list(filter(lambda i: len(at.trie[i]) == 0, range(len(at.trie))))
    argmin=np.argmin([len(at.path(k)) for k in leaves])
    node_I = leaves[argmin]
    pathmin = at.path(node_I)
    pathmin = pathmin[1:]
    node_p = at.locusL(pathmin)

    #nt.G.edge(str(node_p), str(node_I), color = 'green')
    #nt.nEdges += 1
    if (node_I == -1):
        print("found in the process for type L")
    else:
        createMFW(st, node_p, node_I)

    # build MFWs of type I
    # note:  forks stores fork nodes before appending MFW nodes into st
    pathForks = [at.path(i) for i in forks]

#     print("pathForks: ", pathForks)

    for i in range(len(pathForks)):
        path0 = ['0']+pathForks[i]
        path1 = ['1']+pathForks[i]
        if at.locusQ(path0):
            node0 = at.locusL(path0)
            #st.G.edge(str(forks[i]), str(node0), color = 'green')
            #st.nEdges += 1
#             if (node0 == 53):
#                 print("###forks: ", forks)
#                 print("pathForks[{0}]: {1}".format(i, pathForks[i]))
#                 print("node {0}:path {1}".format(node0, path0))
#            print("node0[{0}]@buildADT_SH: {1}".format(node0, st.trie[node0]))

#           if len(nt.trie[node0]) == 0:
#                flagLeaf = True
#
        # exception for type L
        if (not node0 == -1):
#            print("found in the process for type I, 1: path0 {0}".format(path0))
#       else:
            createMFW(st, forks[i], node0)
#
        if st.locusQ(path1):
            node1 = at.locusL(path1)
            #st.G.edge(str(forks[i]), str(node1), color = 'green')
            #st.nEdges += 1

#            print("node1[{0}]@buildADT_SH: {1}".format(node1, st.trie[node1]))
#
#            if len(nt.trie[node1]) == 0:
#                flagLeaf = True
#
        #  exception for type L
        if (not node1== -1):
#            print("found in the process for type I, 1: path1 {0}".format(path1))
#       else:
            createMFW(st, forks[i], node1)
#
    return st
