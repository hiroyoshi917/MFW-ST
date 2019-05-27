#
# -----------------------------------------------------
#  Project Name         : making list of MFWs for text using suffix trie.
#  File Name            : MFW.py
#  Creation Date        : 2019/05/15
#
#  Copy right 2019 Hiroyosh Morita. All rights reserved.
#
#  This source code or any protion thereof must not be
#  reproduced or used in any manner whatsoever.
#

#
# constructor of SuffixTrie
# (2019/05/04)
# (2019/05/13)
#
# (2019/05/14)
# at lecture06
#
# Version:
#   2019/05/23    MFW190523.py
#
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
        self.alph = sorted(list(set(text)))    # make alphabet list
        self.aSize = len(self.alph)
        self.suffixes = self.sortedSuffixes()
        self.build(text)
        self._MFW = []

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

    def view(self, opt='TB'):
        self.G.attr(rankdir=opt)
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
                self.G.node(str(i), shape='square')
#                self.G.attr('node', shape='circle')
            else:
                self.G.node(str(i))
            #
            self.nNodes += 1
            self.degree.append(0)
            self.trie.append({})

        # making edges
        for i in range(len(s)):
#            self.G.edge(str(i), str(i+1), label=str(s[i]))
            self.G.edge(str(i), str(i+1))
            self.G.node(str(i+1), str(s[i]))
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
#                self.G.node(str(nextID+i-lcpv), str(nextID+i-lcpv), shape='square')
                self.G.node(str(nextID+i-lcpv), shape='square')
            else:
#                self.G.node(str(nextID+i-lcpv), str(nextID+i-lcpv))
                self.G.node(str(nextID+i-lcpv))
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
#            self.G.edge(str(prev), str(i), label=s[i-nextID+lcpv])
            self.G.edge(str(prev), str(i))
            self.G.node(str(i), str(s[i-nextID+lcpv]))
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
        p=[-1]*len(self.trie)
        sym = self.alph
        for i in range(len(self.trie)):
            for j in range(self.aSize):
                if sym[j] in self.trie[i]:
                    p[self.trie[i][sym[j]]] = i
        self.parent = copy.copy(p)

    def build(self, src):
        aSuf =  self.getSuffixes(src)
        aSuf.sort()                 # suffixes must be sorted
        aLCP = self.getLCP(aSuf)
        aLCP.append(0)        # add a sentinel

        [nextID, prevPath] = self.firstPathV3(aSuf[0], aLCP[1])

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
        print("alphabet: {0}\t size: {1}".format(self.alph, self.aSize))
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
        sym = self.alph
        if (node < len(self.trie)):
            cn = node
        else:
            return ''
        while cn != -1:
            pn = cn
            cn = self.parent[cn]
            for i in range(len(self.alph)):
                if sym[i] in self.trie[cn] and self.trie[cn][sym[i]] == pn:
                    pathstr.append(sym[i])
        pathstr.reverse()
        return pathstr

    def leafQ(self, id):
         return len(self.trie[id]) == 0

    def printMFW(self):
#        for i in range(len(self._MFW)):
#            print(self._MFW[i])
        for i in range(len(self._MFW)):
            print(self._MFW[i])

    def save(self, opt=''):
        self.G.render(self.text+opt)
#
# methods
#

def createMFWwithBug(nt, pnode, node):
    '''
    create an MFW or MFWs to nt.
    '''
    t = nt.trie
    pList = nt.parent
    n = nt.nNodes
    sym = nt.alph
#     print("in createMFW, pnode: {0}\tnode: {1}".format(pnode, node))

    pathstr = nt.path(node)
    nt.G.attr('node', shape = 'doublecircle')

    for i in range(nt.aSize):
        if sym[i] not in t[node] and sym[i] in t[pnode]:
            mfwStr = pathstr+ [sym[i]]
#            print("MFW: ", mfwStr)
            nt._MFW.append("".join(mfwStr))
            n += 1
#            nt.G.edge(str(node), str(n), label=sym[i], style='bold', color='blue')
            nt.G.edge(str(node), str(n), label=sym[i], style='bold', color='blue')
            nt.G.node(str(n),sym[i])
            t.append({})
            t[node][sym[i]] = n
            nt.parent.append(node)

    nt.G.attr('node', shape = 'circle')
    nt.nNodes = n

def createMFW(atr, ntr, pnode, node):
    '''
    create an MFW or MFWs to nt.
    '''
    oT = atr.trie
    pList = atr.parent
    nT = ntr.trie
    n = ntr.nNodes
    sym = ntr.alph
#     print("in createMFW, pnode: {0}\tnode: {1}".format(pnode, node))

    pathstr = ntr.path(node)
    ntr.G.attr('node', shape = 'doublecircle')

    for i in range(atr.aSize):
        # check this condition on the old trie (HM190523)
        if sym[i] not in oT[node] and sym[i] in oT[pnode]:
            mfwStr = pathstr+ [sym[i]]
#            print("MFW: ", mfwStr)
            ntr._MFW.append("".join(mfwStr))
            n += 1
#            ntr.G.edge(str(node), str(n), label=sym[i], style='bold', color='blue')
            ntr.G.edge(str(node), str(n), style='bold', color='blue')
            ntr.G.node(str(n),sym[i])
            nT.append({})
            nT[node][sym[i]] = n
            ntr.parent.append(node)

    ntr.G.attr('node', shape = 'circle')
    ntr.nNodes = n

def showMFWCandidates(st):
    s = copy.deepcopy(st)
    t = s.trie
    n = len(t)
    sym = st.alph

    for i in range(len(t)):
        for j in range(st.aSize):
            if not sym[j] in t[i]:
                s.G.edge(str(i), str(n), label=sym[j], color='blue')
            n += 1
    s.G.view()

def edgeQ(st, sn, en):
    flag = False
    for i in range(len(st.trie[sn])):
        if (st.alph[i] in st.trie[sn]) and (en == st.trie[sn][st.alph[i]]):
            flag = True
            break
    return flag



def buildADT(st):
    nt = copy.deepcopy(st)
    t = nt.trie
    parent = nt.parent
    forks = nt.forks
    flagLeaf = False
    sym = st.alph

    # build MFWs of type L
    leaves=list(filter(lambda i: len(st.trie[i]) == 0, range(len(st.trie))))
    argmin=np.argmin([len(st.path(k)) for k in leaves])
    node_I = leaves[argmin]
    nt.G.node(str(node_I), color="green")
    pathmin = st.path(node_I)
    pathmin = pathmin[1:]
    node_p = st.locusL(pathmin)

#    if (not edgeQ(nt, node_p, node_I)):
#   L-link
    nt.G.edge(str(node_p), str(node_I), color = 'orange')
    nt.nEdges += 1
    createMFW(st, nt, node_p, node_I)

#    print("pathForks: ", pathForks)
    pathForks = [st.path(i) for i in forks]

    # buile MFWs of type I
    for i in range(len(pathForks)):
        for j in range(st.aSize):
            pathJ = [sym[j]]+pathForks[i]
            if st.locusQ(pathJ):
                nodeJ = st.locusL(pathJ)
                if (not st.leafQ(nodeJ)):     # to avoid to connect a node of type L (190516)
# added label
                    nt.G.edge(str(forks[i]), str(nodeJ), label=sym[j], color = 'green')
                    nt.nEdges += 1
                    createMFW(st, nt, forks[i], nodeJ)

    tmp=sorted(nt._MFW)
    nt._MFW=tmp

    return nt

def buildADT_FH(st):
    nt = copy.deepcopy(st)
    t = nt.trie
    parent = nt.parent
    forks = nt.forks
    flagLeaf = False
    sym = st.alph

    # build MFWs of type I
    pathForks = [nt.path(i) for i in forks]

    for i in range(len(pathForks)):
        for j in range(st.aSize):
            pathJ = [sym[j]]+pathForks[i]
            if st.locusQ(pathJ):
                nodeJ = nt.locusL(pathJ)
                if st.leafQ(nodeJ):         # check if nodeJ is a leaf.
                    nt.G.node(str(nodeJ), color="green")
#                    nt.G.edge(str(forks[i]), str(nodeJ), color = 'orange')
#                else:
                nt.G.edge(str(forks[i]), str(nodeJ), label = sym[j], color = 'green')
                nt.nEdges += 1
                if len(nt.trie[nodeJ]) == 0:
                    flagLeaf = True

    # build MFWs of type L
    if flagLeaf == True:
        return nt

    leaves=list(filter(lambda i: len(st.trie[i]) == 0, range(len(st.trie))))
    argmin=np.argmin([len(st.path(k)) for k in leaves])
    node_I = leaves[argmin]
    nt.G.node(str(node_I), color="green")
    pathmin = st.path(node_I)
    pathmin = pathmin[1:]
    node_p = st.locusL(pathmin)

    nt.G.edge(str(node_p), str(node_I), color = 'orange')
    nt.nEdges += 1
#    createMFW(st, nt, node_p, node_I)

    return nt

def buildADT_SH(at, st):
    '''
    complete AD trie from suffix trie st with MF links
    '''
    nt = copy.deepcopy(st)
    t = at.trie
    parent = at.parent
    forks = at.forks

    # build MFWs of type L

    leaves=list(filter(lambda i: len(t[i]) == 0, range(len(t))))
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
        createMFW(at, nt, node_p, node_I)


    # build MFWs of type I
    # note:  forks stores fork nodes before appending MFW nodes into st
    pathForks = [at.path(i) for i in forks]

#    print("pathForks: ", pathForks)

    alph = at.alph
    for i in range(len(pathForks)):
        for j in range(len(alph)):
            pathJ = [alph[j]]+pathForks[i]
#            if at.locusQ(pathJ):              (stopped here)
            if st.locusQ(pathJ):
                nodeJ = at.locusL(pathJ)
            # exception for type L
            # bug: need one more ident
#           if (not nodeJ == -1):
#               createMFWtemp(at, nt, forks[i], nodeJ)
#            bug: added one more condition
#                if (not nodeJ == -1):
                if (not nodeJ == -1 and not nodeJ == node_I):
                    createMFW(at, nt, forks[i], nodeJ)
#
    tmp=sorted(nt._MFW)
    nt._MFW=tmp

    return nt

#
#   added some more functions
#

#
#   Project: Drawing SuffixTree
#                by Hiroyoshi Morita (2019/05/15)
#
def forkQ(t, node):
    return len(t[node]) > 1

def leafQ(t, node):
    return len(t[node]) == 0

def nodeType(t, node):
    x = len(t[node])
    if x == 0:
        return "LEAF"
    elif x == 1:
        return "LINE"
    elif x > 1:
        return "FORK"

def scanTrie(t, sym, node):
    elabel =""
    nType = nodeType(t, node)
    if nType == "LEAF":
        elabel.append()
    print('node: {0}  t[{0}]: {1} -- type: {2}'.format(node, t[node], nodeType(t,node)))
    printNodeType(t, node)
    for i in range(len(sym)):
#        print("status of sym. '{0}': {1}".format(sym[i], sym[i] in t[node]))
        if sym[i] in t[node]:
            nxtnode = t[node][sym[i]]
            scanTrie(t, sym, nxtnode)

def change_Size_of_Single_Nodes(nt, sym, node):
    if nodeType(nt.trie, node) == "LINE":
        nt.G.node(str(node), str(''), **{'width':str(0.15), 'height':str(0.15)})
    elif nodeType(nt.trie, node) == "LEAF":
        nt.G.node(str(node), str(''), **{'width':str(0.3), 'height':str(0.3)})
    else:
        nt.G.node(str(node), str(''),  **{'width':str(0.3), 'height':str(0.3)})

    for i in range(len(sym)):
#        print("status of sym. '{0}': {1}".format(sym[i], sym[i] in t[node]))
        if sym[i] in nt.trie[node]:
            nxtnode = nt.trie[node][sym[i]]
            change_Size_of_Single_Nodes(nt, sym, nxtnode)

def drawSuffixTree(st, opt='TB'):
    nt = copy.deepcopy(st)
    nt.G.attr(rankdir=opt)
    change_Size_of_Single_Nodes(nt, nt.alph, 0)
    nt.view()
