class Disjunto:
    def __init__(self):
        self.progenitor = {}  # Mapa para almacenar el progenitor de cada nodo
        self.rango = {}  # Mapa para almacenar el rango (profundidad) de cada nodo
    
    def conjunto(self, nodo):
        # Inicializar el nodo, asignando el nodo como su propio progenitor y rango 0
        self.progenitor[nodo] = nodo
        self.rango[nodo] = 0

    def explorar(self, nodo):
        # Recursivamente encontrar el progenitor de un nodo (con compresión de camino)
        if self.progenitor[nodo] != nodo:
            self.progenitor[nodo] = self.explorar(self.progenitor[nodo])
        return self.progenitor[nodo]

    def union(self, nodo1, nodo2):
        # Encontrar los representantes (progenitores) de los dos nodos
        r1 = self.explorar(nodo1)
        r2 = self.explorar(nodo2)

        # Si ya están en el mismo conjunto, no hacer nada
        if r1 != r2:
            # Unión por rango (si el rango de r1 es mayor, r2 se convierte en hijo de r1)
            if self.rango[r1] > self.rango[r2]:
                self.progenitor[r2] = r1
            elif self.rango[r1] < self.rango[r2]:
                self.progenitor[r1] = r2
            else:
                # Si los rangos son iguales, arbitrariamente elige uno como progenitor
                self.progenitor[r2] = r1
                # Aumentar el rango de r1 en caso de que los rangos sean iguales
                self.rango[r1] += 1