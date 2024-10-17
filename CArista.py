class Arista:
    def __init__(self, nodo1, nodo2):
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.atributos = []  # Lista de atributos

    def __eq__(self, other):
        return (self.nodo1.id == other.nodo1.id and self.nodo2.id == other.nodo2.id) or \
               (self.nodo1.id == other.nodo2.id and self.nodo2.id == other.nodo1.id)

    def __hash__(self):
        # Devuelve un hash basado en los IDs de los nodos
        return hash((min(self.nodo1.id, self.nodo2.id), max(self.nodo1.id, self.nodo2.id)))
