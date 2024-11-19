class Arista:
    def __init__(self, nodo1, nodo2, pesos):  
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.pesos = pesos  # Guardamos el peso aquí
        self.atributos = []  # Lista de atributos

    def __repr__(self):
        return f"Arista({self.nodo1.id}, {self.nodo2.id}, {self.pesos})"
    
    def __eq__(self, other):
        # Dos aristas son iguales si tienen los mismos nodos, independientemente de la dirección
        return (self.nodo1 == other.nodo1 and self.nodo2 == other.nodo2) or (self.nodo1 == other.nodo2 and self.nodo2 == other.nodo1)
    
    def __hash__(self):
        # Necesitamos un hash para las aristas, esto es importante para cuando se usan en sets
        return hash(frozenset([self.nodo1.id, self.nodo2.id]))