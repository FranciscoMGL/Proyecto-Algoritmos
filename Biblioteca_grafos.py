from collections import deque
from CNodo import Nodo
from CArista import Arista
import random
import math

class Grafo:
    def __init__(self, dirigido=False):
        self.nodos = {}
        self.aristas = set()  # Usar un conjunto para las aristas
        self.dirigido = dirigido
        self.atributos = []  # Lista de atributos

    def agregar_nodo(self, id):
        if id not in self.nodos:
            self.nodos[id] = Nodo(id)

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

    def agregar_arista(self, nodo1_id, nodo2_id):
        if nodo1_id in self.nodos and nodo2_id in self.nodos:
            arista = Arista(self.nodos[nodo1_id], self.nodos[nodo2_id])
            if self.agregar(arista):  # Asegúrate de llamar al método agregar
                self.nodos[nodo1_id].vecinos.add(self.nodos[nodo2_id])
                if not self.dirigido:
                    self.nodos[nodo2_id].vecinos.add(self.nodos[nodo1_id])  # Para grafos no dirigidos
            else:
                raise ValueError("La arista ya existe.")
        else:
            raise ValueError("Uno de los nodos no existe en el grafo")
    
    def vecinos(self, nodo):
        nodoConectados = []
        for arista in self.aristas:
            if arista.nodo1.id == nodo:  
                nodoConectados.append(arista.nodo2)  
            elif arista.nodo2.id == nodo:
                nodoConectados.append(arista.nodo1)
        
        return nodoConectados
            
    def BFS(self, s):
        arbol_inducido = Grafo(dirigido=self.dirigido)

        if s not in self.nodos:
            raise ValueError("El nodo fuente no existe en el grafo")

        cola = deque([s])
        visitados = {s}
        arbol_inducido.agregar_nodo(s)

        while cola:
            nodo_actual = cola.popleft() 
            for vecino in self.vecinos(nodo_actual):  
                if vecino.id not in visitados:
                    visitados.add(vecino.id)
                    cola.append(vecino.id)
                    arbol_inducido.agregar_nodo(vecino.id) 
                    arbol_inducido.agregar_arista(nodo_actual, vecino.id) 
        
        return arbol_inducido
    
    def DFS_I(self, s):
        arbol_inducido = Grafo(dirigido=self.dirigido)

        if s not in self.nodos:
            raise ValueError("El nodo fuente no existe en el grafo")

        pila = [s]
        visitados = {s}
        arbol_inducido.agregar_nodo(s)

        while pila:
            nodo_actual = pila.pop()
            for vecino in self.vecinos(nodo_actual):
                if vecino.id not in visitados:
                    visitados.add(vecino.id)
                    pila.append(vecino.id)
                    arbol_inducido.agregar_nodo(vecino.id)
                    arbol_inducido.agregar_arista(nodo_actual, vecino.id)

        return arbol_inducido
    
    def DFS_R(self, s):
        arbol_inducido = Grafo(dirigido=self.dirigido)

        if s not in self.nodos:
            raise ValueError("El nodo fuente no existe en el grafo")

        visitados = set()
        arbol_inducido.agregar_nodo(s)

        def dfs_recursivo(nodo):
            visitados.add(nodo)
            for vecino in self.vecinos(nodo):
                if vecino.id not in visitados:
                    visitados.add(vecino.id)
                    arbol_inducido.agregar_nodo(vecino.id)
                    arbol_inducido.agregar_arista(nodo, vecino.id)
                    dfs_recursivo(vecino.id)

        dfs_recursivo(s)
        return arbol_inducido
    
    def guardar_graphviz(self, filename):
        with open(filename, 'w') as f:
            f.write("graph G {\n" if not self.dirigido else "digraph G {\n")

            # Solo agregar nodos que tienen al menos una arista
            nodos_con_aristas = {arista.nodo1.id for arista in self.aristas}.union(
                {arista.nodo2.id for arista in self.aristas}
            )
        
            for nodo_id in nodos_con_aristas:
                f.write(f'  "{nodo_id}";\n')

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

def cargar_grafo_desde_gv(archivo):
    grafo = Grafo()

    with open(archivo, 'r') as f:
        lineas = f.readlines()
    
    nodos = {}

    # Cargar nodos
    for linea in lineas:
        linea = linea.strip()
        if linea.startswith('"') and linea.endswith(';') and not ('--' in linea or '->' in linea):
            nodo_id = linea.replace('"', '').replace(';', '').strip()
            nodo = Nodo(nodo_id)
            grafo.agregar_nodo(nodo)
            nodos[nodo_id] = nodo  # Guardar nodo en el diccionario
    
    # Cargar aristas
    for linea in lineas:
        linea = linea.strip()
        if '--' in linea or '->' in linea:
            aux = linea.replace(';', '').split()
            nodo1_id = aux[0].strip().replace('"', '')
            nodo2_id = aux[-1].strip().replace('"', '')

            if nodo1_id in nodos and nodo2_id in nodos:
                arista = Arista(nodos[nodo1_id], nodos[nodo2_id])
                if grafo.agregar_arista(nodos[nodo1_id], nodos[nodo2_id]):  # Asegúrate de llamar a agregar
                    print(f"Arista agregada: {nodo1_id} -- {nodo2_id}")
                else:
                    print(f"La arista entre {nodo1_id} y {nodo2_id} ya existe.")
            else:
                print(f"Nodos no encontrados para la arista {nodo1_id} <-> {nodo2_id}")

    # Imprimir aristas cargadas para depuración
    print(f"Aristas en el grafo: {[(arista.nodo1.id, arista.nodo2.id) for arista in grafo.aristas]}")  # Verifica las aristas cargadas

    return grafo

def guardar_arbol_en_gv(grafo, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        archivo.write("graph G {\n")
        
        for nodo in grafo.nodos.values():
            for vecino in nodo.vecinos:
                if nodo.id < vecino.id:  # Para evitar duplicados en grafos no dirigidos
                    archivo.write(f'  "{nodo.id}" -- "{vecino.id}";\n')
        
        archivo.write("}\n")

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
