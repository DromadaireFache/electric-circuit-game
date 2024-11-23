import numpy as np

class Node:
    def __init__(self, components: list) -> None:
        self.components: list = components
        self.current = 0
        self.v_dir = {}

    def add(self, component):
        self.components.append(component)

    def combine(self, nodes: list, index: int):
        self.components.extend(nodes[index].component)
        nodes.pop(index)
    
    def __str__(self):
        if len(self.components) == 0: return '[]'
        string = f'{self.current:.2f}A ['
        for component in self.components:
            string += str(component) + ', '
        return string[:-2] + ']'
    
    def __iter__(self):
        return iter(self.components)

class Component:
    def __init__(self, pos=(0,0), vertical = False) -> None:
        self.row, self.col = pos
        self.vertical = vertical
        self.in_node = 0
    
    def part_of(self, node: Node):
        return self in node

class Wire(Component):
    UNITS = 'A'
    def __init__(self, pos=(0, 0), vertical=False, is_ameter=False) -> None:
        super().__init__(pos, vertical)
        self.is_ameter = is_ameter
        if is_ameter:
            self.current = 0

    def __str__(self):
        return f"AM {self.current:.2f}{self.UNITS}" if self.is_ameter else "Wire"
    
    def makenode(self, node: Node, map: list[list[None|Component]], ignore=(0,0)):
        self.in_node = 1
        node.add(self)
        rows = len(map)
        cols = len(map[0])

        if self.row > 0 and ignore[0] != -1 and not (self.is_ameter and not self.vertical): #add the one above
            component: Component = map[self.row-1][self.col]
            # print(component)
            if type(self) is type(component):  #if its a wire continue to make node bigger
                component.makenode(node, map, ignore=(1,0))

            elif component != None and component.vertical: #if its another component just add it to node
                component.in_node += 1
                node.add(component)
                if type(component) is CurrentSource:
                    node.current -= component.I
                elif type(component) is VoltageSource:
                    node.v_dir[component] = np.sign(component.V)
        
        if self.row < rows and ignore[0] != 1 and not (self.is_ameter and not self.vertical): #add the one below
            component: Component = map[self.row+1][self.col]
            # print(component)
            if type(self) is type(component):
                component.makenode(node, map, ignore=(-1,0))

            elif component != None and component.vertical:
                component.in_node += 1
                node.add(component)
                if type(component) is CurrentSource:
                    node.current += component.I
                elif type(component) is VoltageSource:
                    node.v_dir[component] = -np.sign(component.V)
        
        if self.col > 0 and ignore[1] != -1 and not (self.is_ameter and self.vertical): #add the one right
            component: Component = map[self.row][self.col+1]
            # print(component)
            if type(self) is type(component):
                component.makenode(node, map, ignore=(0,1)) 

            elif component != None and not component.vertical:
                component.in_node += 1
                node.add(component)
                if type(component) is CurrentSource:
                    node.current += component.I
                elif type(component) is VoltageSource:
                    node.v_dir[component] = -np.sign(component.V)
        
        if self.col < cols and ignore[1] != 1 and not (self.is_ameter and self.vertical): #add the one left
            component: Component = map[self.row][self.col-1]
            # print(component)
            if type(self) is type(component):
                component.makenode(node, map, ignore=(0,-1))

            elif component != None and not component.vertical:
                component.in_node += 1
                node.add(component)
                if type(component) is CurrentSource:
                    node.current -= component.I
                elif type(component) is VoltageSource:
                    node.v_dir[component] = np.sign(component.V)
    
    def get_current(self, nodes: list[Node], grid, my_node_index: int, x, ignore=(0,0)):
        map = grid.map
        rows = len(map)
        cols = len(map[0])
        current = 0

        if self.row > 0 and ignore[0] != -1 and not (self.is_ameter and not self.vertical) and not ignore == (0,0): #add the one above
            component: Component = map[self.row-1][self.col]
            try:
                current += component.get_current(nodes, grid, my_node_index, x, ignore=(1,0))
            except:
                pass
        
        if self.row < rows and ignore[0] != 1 and not (self.is_ameter and not self.vertical): #add the one below
            component: Component = map[self.row+1][self.col]
            try:
                current += component.get_current(nodes, grid, my_node_index, x, ignore=(-1,0))
            except:
                pass
        
        if self.col > 0 and ignore[1] != -1 and not (self.is_ameter and self.vertical) and not ignore == (0,0): #add the one right
            component: Component = map[self.row][self.col-1]
            try:
                current += component.get_current(nodes, grid, my_node_index, x, ignore=(0,1))
            except:
                pass
        
        if self.col < cols and ignore[1] != 1 and not (self.is_ameter and self.vertical): #add the one left
            component: Component = map[self.row][self.col+1]
            try:
                current += component.get_current(nodes, grid, my_node_index, x, ignore=(0,-1))
            except:
                pass
        
        self.current = current
        return current

class VoltageSource(Component):
    '''aka Battery'''
    UNITS = 'V'
    def __init__(self, pos=(0, 0), vertical=False, volt=0) -> None:
        super().__init__(pos, vertical)
        self.V = volt
    
    def __str__(self):
        return f"VS. {self.V:.2f}{self.UNITS}"
    
    def get_current(self, nodes: list[Node], grid, my_node_index: int, x, ignore=(0,0)):
        index = grid.V_sources().index(self)
        return self.V / x[len(nodes)+index]

class CurrentSource(Component):
    UNITS = 'A'
    def __init__(self, pos=(0, 0), vertical=False, current=0) -> None:
        super().__init__(pos, vertical)
        self.I = current

    def __str__(self):
        return f"CS. {self.I:.2f}{self.UNITS}"
    
    def get_current(self, nodes: list[Node], grid, my_node_index: int, x, ignore=(0,0)):
        return self.I

class Resistor(Component):
    UNITS = 'Ω'
    def __init__(self, pos=(0, 0), vertical=False, res=0, is_light=False) -> None:
        super().__init__(pos, vertical)
        self.R = res
        self.is_light = is_light

    def __str__(self):
        return f"Light {self.R}{self.UNITS}" if self.is_light else f"Res. {self.R}{self.UNITS}"
    
    def W(self, I):
        return I/self.R**2
    
    def get_current(self, nodes: list[Node], grid, my_node_index: int, x, ignore=(0,0)):
        if my_node_index == 0:
            my_voltage = 0
        else:
            my_voltage = x[my_node_index-1]
        
        for i, node in enumerate(nodes):
            if node != nodes[my_node_index] and self in node:
                if i == 0:
                    return - x[my_node_index] / self.R
                return (x[i-1] - my_voltage) / self.R

class Switch(Component):
    def __init__(self, pos=(0, 0), vertical=False) -> None:
        super().__init__(pos, vertical)
        self.closed = False
    
    def switch(self):
        self.closed = not self.closed

def G_matrix(nodes: list[Node]):
    #first wire made is ground, therefore does not go into matrix
    if len(nodes) < 2: return None
    nodes = nodes[1:]
    G = np.zeros((len(nodes), len(nodes)))

    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            sum_ = 0
            if i == j:
                for component in node1:
                    try:
                        sum_ += 1 / component.R
                    except:
                        continue
            else:
                for component in node1:
                    if component in node2:
                        try:
                            sum_ -= 1 / component.R
                        except:
                            continue
            G[i,j] = sum_
    
    return G

def current_vector(nodes: list[Node]):
    nodes = nodes[1:]
    i = np.zeros((len(nodes)))
    for k, node in enumerate(nodes):
        i[k] = node.current
    return i

def voltage_dir(nodes: list[Node], V_sources):
    nodes = nodes[1:]
    B = np.zeros((len(nodes), len(V_sources)))

    for i, node in enumerate(nodes):
        for j, v in enumerate(V_sources):
            if v in node:
                B[i, j] = node.v_dir[v]

    return B

def A_matrix(nodes: list[Node], v_sources):
    G = G_matrix(nodes)
    B = voltage_dir(nodes, v_sources)
    C = B.transpose()
    D = np.zeros((len(v_sources),len(v_sources)))
    return np.block([[G, B],[C,D]])

def z_matrix(nodes: list[Node], v_sources: list[VoltageSource]):
    i = current_vector(nodes)
    e = np.zeros((len(v_sources)))
    for k, v_source in enumerate(v_sources):
        e[k] = abs(v_source.V)
    
    return np.concatenate((i,e), axis=0)

def x_matrix(nodes: list[Node], v_sources: list[VoltageSource]):
    A = A_matrix(nodes, v_sources)
    z = z_matrix(nodes, v_sources)
    return np.linalg.inv(A) @ z

class Grid:
    DISSIZE = 12
    def __init__(self, cols, rows) -> None:
        self.map: list[list[None|Component|Wire]] = [[None for j in range(cols)] for i in range(rows)]
        self.rows = rows
        self.cols = cols
    
    def place(self, component: Component):
        self.map[component.row][component.col] = component

    def remove(self, pos:tuple[int,int]|None=None):
        '''Leave pos argument empty to delete everything, otherwise specify (row,col)'''
        if pos == None:
            self.map = [[None for j in range(self.cols)] for i in range(self.rows)]
        else:
            self.map[pos[0]][pos[1]] = None

    def __str__(self):
        string = ''.rjust(self.rows*(Grid.DISSIZE+1)+1,'-') + '\n'
        for row in self.map:
            for component in row:
                if component == None:
                    string += '|' + ''.rjust(Grid.DISSIZE, ' ')
                else:
                    string += '|' + str(component).rjust(Grid.DISSIZE, ' ')
            string += '|\n'
            string += ''.rjust(self.rows*(Grid.DISSIZE+1)+1,'-') + '\n'
        return string
    
    def find_nodes(self) -> list[Node]:
        nodes: list[Node] = []
        for row in self.map:
            for component in row:
                if component == None: continue #don't consider empty tiles
                component.in_node = 0
        
        for row in self.map:
            for component in row:
                if component == None or component.in_node != 0: continue

                if isinstance(component, Wire):
                    nodes.append(Node([]))
                    component.makenode(nodes[-1], self.map)
        
        #TO REMOVE COMPONENTS NOT CONNECTED TWICE
        for i, node in enumerate(nodes):
            for j, component in enumerate(node):
                if component.in_node != 2 and not type(component) is Wire:
                    nodes[i].components.pop(j)

        return nodes
    
    def __iter__(self):
        return iter(self.map)
    
    def V_sources(self):
        V_sources_list = []
        for row in self:
            for component in row:
                if type(component) is VoltageSource:
                    V_sources_list.append(component)
        return V_sources_list
    
    def get_currents(self, nodes:list[Node]):
        x = x_matrix(nodes, self.V_sources())
        for i, node in enumerate(nodes):
            for component in node.components:
                if type(component) is Wire and component.is_ameter:
                    component.get_current(nodes, self, i, x)
    
if __name__ == '__main__':
    grid = Grid(11, 11)
    
    grid.place(Resistor((3,2), True, res=1))
    grid.place(Resistor((3,4), True, res=2))
    grid.place(Resistor((5,4), True, res=3))
    grid.place(Resistor((5,6), True, res=4, is_light=True))
    grid.place(Resistor((4,7), res=5))
    grid.place(Resistor((1,1), True, res=100))

    grid.place(CurrentSource((3,1), True, current=1))
    grid.place(VoltageSource((6,7), volt=-1))

    grid.place(Wire((2,1)))
    grid.place(Wire((4,1)))
    grid.place(Wire((4,4)))
    grid.place(Wire((4,5)))
    grid.place(Wire((4,6)))
    grid.place(Wire((6,4)))
    grid.place(Wire((6,5), False, is_ameter=True))
    grid.place(Wire((6,6)))
    grid.place(Wire((2,2)))
    grid.place(Wire((2,3), False, is_ameter=True))
    grid.place(Wire((2,4)))
    grid.place(Wire((4,2)))
    grid.place(Wire((4,3)))
    grid.place(Wire((4,8)))
    grid.place(Wire((5,8)))
    grid.place(Wire((6,8)))
    nodes = grid.find_nodes()
    grid.get_currents(nodes)
    print(grid)
    for node in nodes: print(node)

    # G = G_matrix(nodes)
    # print(G)
    # inv_G = np.linalg.inv(G)
    # i = current_vector(nodes)
    # print(i)
    # print(inv_G @ i)

    print(x_matrix(nodes, grid.V_sources()))