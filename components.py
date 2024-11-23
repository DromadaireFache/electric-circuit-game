import numpy as np

class Node:
    def __init__(self, components: list) -> None:
        self.components: list = components

    def add(self, component):
        self.components.append(component)

    def combine(self, nodes: list, index: int):
        self.components.extend(nodes[index].component)
        nodes.pop(index)
    
    def __str__(self):
        if len(self.components) == 0: return '[]'
        string = '['
        for component in self.components:
            string += str(component) + ', '
        return string[:-2] + ']'

class Component:
    def __init__(self, pos=(0,0)) -> None:
        self.row, self.col = pos
        self.in_node = False
    
    def part_of(self, node: Node):
        return self in node.components

class Wire(Component):
    def __init__(self, pos=(0, 0)) -> None:
        super().__init__(pos)

    def __str__(self):
        return "Wire"
    
    def makenode(self, node: Node, map: list[list[None|Component]], ignore=(0,0)):
        self.in_node = True
        # node.add(self)
        rows = len(map)
        cols = len(map[0])

        if self.row > 0 and ignore[0] != -1: #add the one above
            component: Component = map[self.row-1][self.col]
            # print(component)
            if type(self) is type(component):  #if its a wire continue to make node bigger
                component.makenode(node, map, ignore=(1,0)) 

            elif component != None: #if its another component just add it to node
                component.in_node = True
                node.add(component)
        
        if self.row < rows and ignore[0] != 1: #add the one below
            component: Component = map[self.row+1][self.col]
            # print(component)
            if type(self) is type(component):
                component.makenode(node, map, ignore=(-1,0))

            elif component != None:
                component.in_node = True
                node.add(component)
        
        if self.col > 0 and ignore[1] != -1: #add the one right
            component: Component = map[self.row][self.col-1]
            # print(component)
            if type(self) is type(component):
                component.makenode(node, map, ignore=(0,1)) 

            elif component != None:
                component.in_node = True
                node.add(component)
        
        if self.col < cols and ignore[1] != 1: #add the one left
            component: Component = map[self.row][self.col+1]
            # print(component)
            if type(self) is type(component):
                component.makenode(node, map, ignore=(0,-1))

            elif component != None:
                component.in_node = True
                node.add(component)

class VoltageSource(Component):
    '''aka Battery'''
    UNITS = 'V'
    def __init__(self, pos=(0, 0), volt=0) -> None:
        super().__init__(pos)
        self.V = volt

class CurrentSource(Component):
    UNITS = 'A'
    def __init__(self, pos=(0, 0), current=0) -> None:
        super().__init__(pos)
        self.I = current

class Resistor(Component):
    UNITS = 'Ω'
    def __init__(self, pos=(0, 0), res=0) -> None:
        super().__init__(pos)
        self.R = res

    def __str__(self):
        return f"Res. {self.R}{Resistor.UNITS}"

class Light(Component):
    UNITS = 'W'
    def __init__(self, pos=(0, 0), power=0) -> None:
        super().__init__(pos)
        self.P = power

class Switch(Component):
    def __init__(self, pos=(0, 0)) -> None:
        super().__init__(pos)
        self.closed = False
    
    def switch(self):
        self.closed = not self.closed

# try:
#     inverse_matrix = np.linalg.inv(matrix)
#     print("Matrix:\n", matrix)
#     print("Inverse Matrix:\n", inverse_matrix)
# except np.linalg.LinAlgError:
#     print("Matrix is singular and cannot be inverted.")

def create_matrix(nodes: list[Node]):
    #first wire made is ground, therefore does not go into matrix
    G = np.zeros((len(nodes)-1, len(nodes)-1))

    for i, node1 in enumerate(start=1):
        for j, node2 in enumerate(start=1):
            if i == j:
                pass

class Grid:
    DISSIZE = 12
    def __init__(self, cols, rows) -> None:
        self.map: list[list[None|Component|Wire]]= [[None for j in range(cols)] for i in range(rows)]
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
        nodes = []
        for row in self.map:
            for component in row:
                if component == None: continue #don't consider empty tiles
                component.in_node = False
        
        for row in self.map:
            for component in row:
                if component == None or component.in_node: continue

                if isinstance(component, Wire):
                    nodes.append(Node([]))
                    component.makenode(nodes[-1], self.map)

        return nodes

if __name__ == '__main__':
    grid = Grid(10, 10)
    
    grid.place(Resistor((5,4), 100))
    grid.place(Resistor((5,6), 50))
    grid.place(Resistor((3,4), 150))
    grid.place(Resistor((3,2), 200))
    grid.place(Wire((4,4)))
    grid.place(Wire((4,5)))
    grid.place(Wire((4,6)))
    grid.place(Wire((6,4)))
    grid.place(Wire((6,5)))
    grid.place(Wire((6,6)))
    
    grid.place(Wire((2,2)))
    grid.place(Wire((2,3)))
    grid.place(Wire((2,4)))
    grid.place(Wire((4,2)))
    grid.place(Wire((4,3)))
    print(grid)
    nodes = grid.find_nodes()
    for node in nodes: print(node)