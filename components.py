import numpy as np

class Node:
    def __init__(self, components: list) -> None:
        self.components: list = components

    def add(self, component):
        self.components.append(component)

    def combine(self, nodes: list, index: int):
        self.components.extend(nodes[index].component)
        nodes.pop(index)

class Component:
    def __init__(self, nodes: tuple[Node,Node], pos = (0,0)) -> None:
        self.row, self.col = pos
        nodes[0].add(self)
        nodes[1].add(self)

class Wire:
    def __init__(self, node: Node, pos=(0, 0)) -> None:
        self.row, self.col = pos
        node.add(self)

class VoltageSource(Component):
    '''aka Battery'''
    UNITS = 'V'
    def __init__(self, nodes: tuple[Node,Node], pos=(0, 0), volt=0) -> None:
        super().__init__(nodes, pos)
        self.V = volt

class CurrentSource(Component):
    UNITS = 'A'
    def __init__(self, nodes: tuple[Node,Node], pos=(0, 0), current=0) -> None:
        super().__init__(nodes, pos)
        self.I = current

class Resistor(Component):
    UNITS = 'Ω'
    def __init__(self, nodes: tuple[Node,Node], pos=(0, 0), res=0) -> None:
        super().__init__(nodes, pos)
        self.R = res

class Light(Component):
    UNITS = 'W'
    def __init__(self, nodes: list[Node], pos=(0, 0), power=0) -> None:
        super().__init__(nodes, pos)
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
    G = np.zeros((len(nodes)-1, len(nodes)-1))

    for i, node1 in enumerate(nodes, start=1):
        for j, node2 in enumerate(nodes, start=1):
            if i == j:
                pass

if __name__ == '__main__':
    #first wire made is ground, therefore does not go into matrix
    nodes = [Node([]) for i in range(10)]
    r1 = Resistor([nodes[0], nodes[5]], (0,0), 100)