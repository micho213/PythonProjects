# Michal Wolas 117308883

from time import perf_counter


class Element:
    def __init__(self, k, v, i):
        self._key = k  # Vertex
        self._value = v  # cost to get there
        self._index = i  # position in the APQ heap list

    # checks if two elements are equal by value
    def __eq__(self, other):
        return self._value == other._value

    # checks if two elements are < less than by value as key is vertex
    def __lt__(self, other):
        return self._value < other._value

    # to print the element value
    def __str__(self):
        return str(self._value)

    def _wipe(self):  # clean remove the element
        self._key = None
        self._value = None
        self._index = None


# Adaptable priority queue, implemented with Binary heap,
# with bubble up and bubble down iterative versions
class APQ:
    def __init__(self):
        self._APQ = []

    # changes the value of an element, and refinances up
    # because if a change occurs it only occurs if the value has improved
    def update_key(self, element, new_value):
        element._value = new_value
        self.rebalanceUP(element._index)

    def get_value(self, element):
        return element._value  # return the key for the element


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
            else:  # if there was no swap it means its in the right place -  quit
                break

    # string method , mainly for testing
    def __str__(self):
        if len(self._APQ) > 100:
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
        self._APQ.pop(end)  # remove last element
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
                    self._APQ[position], self._APQ[item] = self._APQ[item], self._APQ[position]
                    self._APQ[position]._index = item
                    self._APQ[item]._index = position
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


#
class Vertex:
    def __init__(self, element, GPS):
        self.element = element
        self.GPS = GPS  # tuple of (latitude,longitude)

    def __str__(self):
        return str(self.element)

    def element(self):
        return self

    def __lt__(self, v):
        return self.element < v.element


# Edge between two vertices, containing its weight(time to get there)
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

    # returns the opposite vertex of x
    def opposite(self, x):
        if x in self.edge:
            if x == self.edge[0]:
                return self.edge[1]
            else:
                return self.edge[0]
        return None

    def element(self):  # the edges element is the weight it has
        return self.weight

    def __str__(self):
        return str(self.weight)


class RouteMap:
    def __init__(self):
        self.map = {}  # main structure for the graph
        self.elements = {}  # has the elements for efficient lookup to get a vertex by label
        # necessary structures for dijkstra's
        self.open = APQ()
        self.locs = {}
        self.closed = {}
        self.preds = {}

    def __str__(self):
        if len(self.map) > 100:
            return "Too big to print, sorry"
        return self.print(self.map)

    # prints the graph in somewhat readable format
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

    # returns a list of edges from vertex x
    def get_edges(self, x):
        connectedVertices = self.map[x]
        edges = []
        for edge in connectedVertices:
            edges += [self.map[x][edge]]
        return edges

    # returns the vertex at a given label/id
    def get_vertex_by_label(self, label):
        return self.elements[label]

    # adds a vertex to the graph
    def add_vertex(self, vertex, GPS=None):
        # if the given vertex is already a vertex class, just add it
        if isinstance(vertex, Vertex):
            self.map[vertex] = {}
            self.elements[vertex.element] = vertex
        else:  # create an instance
            v = Vertex(vertex, GPS)
            self.map[v] = {}
            self.elements[v.element] = v


    def add_edge(self, x, y, edge):
        # if edge is already an instance of edge
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
            v = min_el._key  # key gives the reference to the Vertex class instance
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

    # shortest path from v to w
    def sp(self, v, w):
        if v.element == w.element:
            print("already here")
            return [],[]
        closed = self.dijkstra(v)
        path = []  # has the vertices from w to v
        costs = []  # has the corresponding cost
        next_v = closed[w][1]
        cost = closed[w][0]
        while True:
            if next_v != None:
                cost = closed[next_v][0]
            else:
                cost = 0
            if next_v.element == v.element:  # if the starting vertex as been met
                path += [next_v]
                costs += [cost]
                path = path[::-1]
                costs = costs[::-1]
                break
            path += [next_v]
            costs += [cost]
            next_v = closed[next_v][1]
        return path , costs

    # print out results for the GPS visualizer2
    def GPSVisualiserPrint(self,path,costs):
        result = zip(path, costs)
        print("type \t latitude \t longitude \t element \t cost ")
        for vertex, cost in result:
            print("w \t %f \t %f \t %d \t %f " % (vertex.GPS[0], vertex.GPS[1], vertex.element, cost ))


def graphreader(filename):
    """ Read and return the route map in filename. """
    graph = RouteMap()
    file = open(filename, 'r')
    entry = file.readline()  # either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        nodeGPS = file.readline().split()

        graph.add_vertex(nodeid, (float(nodeGPS[1]), float(nodeGPS[2])))
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
        time = float(file.readline().split()[1])
        graph.add_edge(sv, tv, time)
        file.readline()  # read the one-way data
        entry = file.readline()  # either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')

    return graph


def test():
    ids = {}
    ids['wgb'] = 1669466540
    ids['turnerscross'] = 348809726
    ids['neptune'] = 1147697924
    ids['cuh'] = 860206013
    ids['oldoak'] = 358357
    ids['gaol'] = 3777201945
    ids['mahonpoint'] = 330068634
    sourcestr = 'mahonpoint'
    deststr='cuh'
    x1 = perf_counter()
    graph = graphreader("corkCityData.txt")
    source = graph.get_vertex_by_label(ids[sourcestr])
    dest = graph.get_vertex_by_label(ids[deststr])
    path, costs = graph.sp(source, dest)
    x2 = perf_counter()
    print(x2 - x1, " time took build graph and run dijkstra, and make the shortest path")
    graph.GPSVisualiserPrint(path,costs)


test()


