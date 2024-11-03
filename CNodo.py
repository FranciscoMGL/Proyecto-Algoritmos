class Nodo:
    def __init__(self, id):
        self.id = id
        self.aristas = set()
        self.vecinos = set()
        self.atributos = []  
        
    def __repr__(self):
        return f"Nodo({self.id})"
    
    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id  # Compare based on the id
    
    def __hash__(self):
        return hash(self.id)