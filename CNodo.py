class Nodo:
    def __init__(self, id):
        self.id = id
        self.aristas = set()
        self.atributos = []  # Lista de atributos
    
    def __repr__(self):
        return f"Nodo(id={self.id}, aristas={len(self.aristas)}, atributos={self.atributos})"
    
    def __eq__(self,other):
        if isinstance(other, Nodo):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash(self.id)
    