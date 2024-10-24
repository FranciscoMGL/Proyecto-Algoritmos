from CNodo import Nodo
from CArista import Arista
import random
import math

class Grafo:
    def __init__(self, dirigido=False):
        self.nodos = []
        self.aristas = set()  # Usar un conjunto para las aristas
        self.dirigido = dirigido
        self.atributos = []  # Lista de atributos

    def agregar_nodo(self, nodo):
        if nodo not in self.nodos:
            self.nodos.append(nodo)

    def existe_arista(self, arista):
        if self.dirigido:
            return arista in self.aristas
        else:
            return arista in self.aristas or Arista(arista.nodo2, arista.nodo1) in self.aristas
   
    def agregar(self, arista):
        if not self.existe_arista(arista):
            self.aristas.add(arista)  # Añadir directamente al conjunto
            arista.nodo1.aristas.add(arista )
            arista.nodo2.aristas.add(arista )
            return True
        return False

    def agregar_arista(self, arista):
        if not self.existe_arista(arista):
            self.aristas.add(arista)  # Añadir directamente al conjunto

    def guardar_graphviz(self, filename):
        with open(filename, 'w') as f:
            f.write("graph G {\n" if not self.dirigido else "digraph G {\n")
            for nodo in self.nodos:
                f.write(f'  "{nodo.id}";\n')

            for arista in self.aristas:
                if self.dirigido:
                    f.write(f'    "{arista.nodo1.id}" -> "{arista.nodo2.id}";\n')
                else:
                    f.write(f'    "{arista.nodo1.id}" -- "{arista.nodo2.id}";\n')
            f.write("}\n")

    def mostrar_grafo(self):
        print(f"Grafo {'dirigido' if self.dirigido else 'no dirigido'} creado con {len(self.nodos)} nodos y {len(self.aristas)} aristas.")

    def grado_nodo(self, nodo):
        if nodo in self.nodos:
            return len(nodo.aristas)
        return 0
    
def grafoMalla(m, n, dirigido=False):
    """Genera un grafo de malla de tamaño m x n."""
    if m <= 1 or n <= 1:
        raise ValueError("Los valores de m y n deben ser mayores que 1.")

    grafo = Grafo(dirigido)
    nodos = [[Nodo(f"n{i}_{j}") for j in range(n)] for i in range(m)]
    
    for i in range(m):
        for j in range(n):
            grafo.agregar_nodo(nodos[i][j])
            if i < m - 1:
                grafo.agregar_arista(Arista(nodos[i][j], nodos[i + 1][j]))
            if j < n - 1:
                grafo.agregar_arista(Arista(nodos[i][j], nodos[i][j + 1]))
    
    return grafo

def grafoErdosRenyi(n, m, dirigido=False):
    """Genera un grafo aleatorio según el modelo Erdös-Rényi."""
    if n <= 0:
        raise ValueError("El número de nodos debe ser mayor que 0.")
    if m < n - 1:
        raise ValueError("El número de aristas debe ser al menos n-1.")

    grafo = Grafo(dirigido)
    nodos = [Nodo(i) for i in range(n)]
    
    for nodo in nodos:
        grafo.agregar_nodo(nodo)

    aristas = set()

    for i in range(n-1):
        arista = Arista(nodos[i], nodos[i+1])
        aristas.add(arista)
        grafo.agregar_arista(arista)
    
    while len(aristas) < m:
        n1, n2 = random.sample(range(n), 2)
        if n1 == n2:
            continue

        arista = Arista(nodos[n1], nodos[n2])
    
        if not dirigido and (arista in aristas or Arista(nodos[n2], nodos[n1]) in aristas):
          continue

        aristas.add(arista)
        grafo.agregar_arista(arista)

    return grafo

def grafoGilbert(n, p, dirigido=False):
    """Genera un grafo aleatorio según el modelo Gilbert."""
    if n <= 0:
        raise ValueError("El número de nodos debe ser mayor que 0.")
    if not (0 < p < 1):
        raise ValueError("La probabilidad p debe estar entre 0 y 1.")

    grafo = Grafo(dirigido)
    nodos = [Nodo(i) for i in range(n)]
    
    for nodo in nodos:
        grafo.agregar_nodo(nodo)

    for i in range(n):
        for j in range(n):
            if i != j:
                if random.random() < p:
                    grafo.agregar_arista(Arista(nodos[i], nodos[j]))

    return grafo

def grafoGeografico(n, r, dirigido=False):
    """Genera un grafo aleatorio según el modelo geográfico.""" 
    if n <= 0:
        raise ValueError("El número de nodos debe ser mayor que 0.")
    if not (0 < r <= 1):
        raise ValueError("La distancia r debe estar entre 0 y 1.")

    grafo = Grafo(dirigido)
    posiciones = [(random.random(), random.random()) for _ in range(n)]
    nodos = [Nodo(i) for i in range(n)]
    
    for nodo in nodos:
        grafo.agregar_nodo(nodo)

    for i in range(n):
        for j in range(i + 1, n):
            distancia = math.sqrt((posiciones[i][0] - posiciones[j][0]) ** 2 +
                                  (posiciones[i][1] - posiciones[j][1]) ** 2)
            if distancia <= r:
                grafo.agregar_arista(Arista(nodos[i], nodos[j]))
                if not dirigido:
                    grafo.agregar_arista(Arista(nodos[j], nodos[i]))

    return grafo

def grafoBarabasiAlbert(n, d, dirigido=False, auto=False):
    
    if n < 1 or d < 2:
        raise ValueError("Error: n > 0 y d > 1")
    
    grafo = Grafo(dirigido)
    nodos_deg = dict() # Diccionario para llevar el conteo del grado de cada nodo.
    
    # Crear nodos
    for nodo_id in range(n):
        nodo = Nodo(nodo_id)
        grafo.agregar_nodo(nodo)
        nodos_deg[nodo_id] = 0
    
    nodos = grafo.nodos
    
    # Agregar aristas al azar, con cierta probabilidad
    for nodo in nodos:
        for v in nodos:
            if nodos_deg[nodo.id] == d:
                break
            if nodos_deg[v.id] == d:
                continue
            p = random.random()
            equal_nodes = v == nodo
            if equal_nodes and not auto:
                continue

            if p <= 1 - nodos_deg[v.id] / d and grafo.agregar(Arista(nodo, v)):
                nodos_deg[nodo.id] += 1
                if not equal_nodes:
                    nodos_deg[v.id] += 1

    return grafo

def grafoDorogovtsevMendes(n, dirigido=False):
    """Genera un grafo según el modelo Dorogovtsev-Mendes.""" 
    if n < 3:
        raise ValueError("El número de nodos debe ser al menos 3.")

    grafo = Grafo(dirigido)
    
    # Inicializa un triángulo
    nodos = [Nodo(i) for i in range(3)]
    for nodo in nodos:
        grafo.agregar_nodo(nodo)
    grafo.agregar_arista(Arista(nodos[0], nodos[1]))
    grafo.agregar_arista(Arista(nodos[1], nodos[2]))
    grafo.agregar_arista(Arista(nodos[0], nodos[2]))

    # Agregar nodos adicionales
    for i in range(3, n):
        nuevo_nodo = Nodo(i)
        grafo.agregar_nodo(nuevo_nodo)
        arista_random = random.choice(list(grafo.aristas))  # Convertir a lista para elegir al azar
        grafo.agregar_arista(Arista(nuevo_nodo, arista_random.nodo1))
        grafo.agregar_arista(Arista(nuevo_nodo, arista_random.nodo2))

    return grafo
