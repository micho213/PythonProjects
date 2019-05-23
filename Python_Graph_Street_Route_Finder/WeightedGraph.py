
class Element:
    def __init__(self, k, v, i):
        self._key = k   # Vertex
        self._value = v # cost to get there
        self._index = i # position in the APQ heap list

    # checks if two elements are equal by value
    def __eq__(self, other):
        return self._value == other._value

    # checks if two elements are < less than by value as key is vertex
    def __lt__(self, other):
        return self._value < other._value

    # to print the element value
    def __str__(self):
        return str(self._value)

    def _wipe(self): # clean remove the element
        self._key = None
        self._value = None
        self._index = None


class APQ:
    def __init__(self):
        self._APQ = []

    # O(log n)
    # changes the value of an element, and refinances up
    # because if a change occurs it only occurs if the value has improved
    def update_key(self, element, new_value):
        element._value = new_value
        self.rebalanceUP(element._index)

    # O(1)  return value of an element
    def get_value(self, element):
        return element._value  # return the key for the element


    # O (log n )
    def add(self, key, item):
        new_element = Element(key, item, len(self._APQ))
        self._APQ.append(new_element)
        self.rebalanceUP(len(self._APQ) - 1)
        return new_element

    # iterative bubble up
    def rebalanceUP(self, i):
        parent = (i - 1) // 2
        while parent > 0:
            parent = (i - 1) // 2
            if self._APQ[i] < self._APQ[parent]:
                # update the swapped elements index
                self._APQ[parent]._index = i
                self._APQ[i]._index = parent
                #swap the elements in the list
                self._APQ[parent], self._APQ[i] = self._APQ[i], self._APQ[parent]
                i = parent
            else: # if there was no swap it means its in the right place -  quit
                break

    # string method , mainly for testing
    def __str__(self):
        if len( self._APQ) > 100:
            return "cannot print, too large"
        heap = ""
        for i in self._APQ:
            heap += str(i) + " , "
        return heap

    # O(log n) , returns and removes minimal value from APQ
    def remove_min(self):
        if len(self._APQ) == 0:
            return None
        # min value always at 0
        min = self._APQ[0]
        end = len(self._APQ) - 1
        # place last element on the top
        self._APQ[0] = self._APQ[end]
        self._APQ.pop(end) # remove last element
        item = 0
        self.rebalanceDown(item, end)
        return min

    def rebalanceDown(self, item, end):
        while (item * 2 + 1) < end:
            # if it ever enters the loop then left child exits, position is left child, position +1 is rightchild
            position = (2 * item) + 1
            lchild = self._APQ[position]._value

            # if right child exists compare left with right and decide
            if end - 1 > position:
                rchild = self._APQ[position + 1]._value  # right child exists

                if lchild <= rchild:
                    if self._APQ[item]._value > lchild:  # if the item we are bubbling is smaller swap
                        self._APQ[position]._index = item
                        self._APQ[item]._index = position
                        self._APQ[position], self._APQ[item] = self._APQ[item], self._APQ[position]

                        item = position  # position updated for the next loop iteration
                    else:
                        break
                else:  # same as above but for rightchild
                    if self._APQ[item]._value > rchild:
                        self._APQ[position + 1]._index = item
                        self._APQ[item]._index = position + 1
                        self._APQ[position + 1], self._APQ[item] = self._APQ[item], self._APQ[position + 1]

                        item = position + 1
                    else:
                        break
            # if there isn't a rightchild, only check left child
            else:
                if self._APQ[item]._value > lchild:
                    self._APQ[position]._index = item
                    self._APQ[item]._index = position
                    self._APQ[position], self._APQ[item] = self._APQ[item], self._APQ[position]

                    item = position
                else:
                    break  # must be in the right position so break out

    # O(log n)*
    def min(self):
        return self._APQ[0]

    def is_empty(self):
        if self._APQ == []:
            return True
        return False

    def length(self):
        return len(self._APQ)

# vertex class, stores the element value/name of the vertex
class Vertex:
    def __init__(self, element):
        self.element = element

    def __str__(self):
        return str(self.element)

    def element(self):
        return self

    def __lt__(self, v):
        return self.element < v.element


class Edge:
    def __init__(self, edge, weight):
        self.edge = edge  # tuple of 2 vertices
        self.weight = weight

    def vertices(self):
        return self.edge[0], self.edge[1]

    def vertex1(self):
        return self.edge[0]

    def vertex2(self):
        return self.edge[1]

    # find the opposing vertex
    def opposite(self, x):
        if x in self.edge:
            if x == self.edge[0]:
                return self.edge[1]
            else:
                return self.edge[0]
        return None

    def element(self):
        return self.weight

    def __str__(self):
        return str(self.weight)


class Graph:
    def __init__(self):
        self.map = {}
        self.elements = {}
        # data structures for dijkstras
        self.open = APQ()
        self.locs = {}
        self.closed = {}
        self.preds = {}

    def __str__(self):
        return self.print(self.map)

    def print(self, map):
        result = "What each vertex joins with: \n"
        i = 0
        for k in map:
            result += str(k) + " : " + str(k) + "---"
            for k2 in map[k]:
                result += str(k2) + "( " + str(map[k][k2]) + " )  "
                i += 1
                if len(map[k]) > 1 and i < len(map[k]):
                    result += str(k) + "---"
            result += "\n"
            i = 0
        return result

    # return the edges incident on the vertex x
    def get_edges(self, x):
        connectedVertices = self.map[x]
        edges = []
        for edge in connectedVertices:
            edges += [self.map[x][edge]]
        return edges

    # get vertex by its element
    def get_vertex_by_label(self, element):
        return self.elements[element]

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex):
            self.map[vertex] = {}
            self.elements[vertex.element] = vertex
        else:
            v = Vertex(vertex)
            self.map[v] = {}
            self.elements[v.element] = v


    def add_edge(self, x, y, edge):
        if not isinstance(edge, Edge):
            edge = Edge((x, y), edge)

        xmap = self.map[x]
        xmap[y] = edge

        ymap = self.map[y]
        ymap[x] = edge

    # provides shortest path to every other node from starting ndoe s
    def dijkstra(self, s):
        # initializing

        self.open = APQ()
        self.locs = {}
        self.closed = {}
        self.preds = {}
        # s : None is the initial starting point, preds, locs and open have it
        self.preds = {s: None}
        startingPoint = self.open.add(s, 0)
        self.locs[s] = startingPoint

        while not self.open.is_empty():
            # min_el an instance of the element class, that has the minimum value from APQ open
            min_el = self.open.remove_min()
            v = min_el._key # key gives the reference to the Vertex class instance
            self.locs.pop(v)
            predecessor = self.preds.pop(v)

            # min_el._value is the cost of getting to that element
            self.closed[v] = (min_el._value, predecessor)

            # for each edge from v (the min element )
            for e in self.get_edges(v):
                w = e.opposite(v)
                if w not in self.closed:
                    newcost = min_el._value + e.weight
                    if w not in self.locs:

                        self.preds[w] = v
                        new_el = self.open.add(w, newcost)
                        self.locs[w] = new_el
                    elif newcost < (self.locs[w]._value):

                        self.preds[w] = v
                        self.open.update_key(self.locs[w], newcost)
        return self.closed

def graphreader(filename):
    """ Read and return the route map in filename. """
    graph = Graph()
    file = open(filename, 'r')
    entry = file.readline()  # either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        graph.add_vertex(nodeid)
        entry = file.readline()  # either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        length = float(file.readline().split()[1])
        graph.add_edge(sv, tv, length)
        file.readline()  # read the one-way data
        entry = file.readline()  # either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')

    return graph



graph = graphreader("simplegraph2.txt")
search = graph.get_vertex_by_label(14)
end = graph.get_vertex_by_label(5)
closed = graph.dijkstra(search)


# a simplified version of sp for first part
def tracePath(closed, v1, v2):
    # v1 = s , as passed into dijkstra
    # v2 is where we want to get to
    print("path from %s to %s " % (v1,v2))
    path = [str(v2) + " cost: " + str(closed[v2][0])]
    backwards_search  = v2
    next = closed[v2][1]
    while True:
        path += [str(next)]
        next =closed[next][1]
        if next == v1:
            path += ["start: " + str(next)]
            return path[::-1]

x = tracePath(closed,search,end)
print(x)

