class Arista:
    def __init__(self, nodo1, nodo2):
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.atributos = []

    def __hash__(self):
        return hash((min(self.nodo1.id, self.nodo2.id), max(self.nodo1.id, self.nodo2.id)))

    def __eq__(self, other):
        return (self.nodo1 == other.nodo1 and self.nodo2 == other.nodo2) or \
               (self.nodo1 == other.nodo2 and self.nodo2 == other.nodo1)

