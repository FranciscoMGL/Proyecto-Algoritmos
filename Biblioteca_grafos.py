from CNodo import Nodo
from CArista import Arista
import heapq
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
        """ Verifica si existe una arista en el grafo (considerando que el grafo puede ser dirigido o no). """
        if self.dirigido:
            # Para grafos dirigidos, buscamos la arista tal cual (con su peso)
            return arista in self.aristas
        else:
            # Para grafos no dirigidos, buscamos la arista o la versión invertida
            # Calculamos el peso por defecto
            pesos_default = 1.0  # O el valor predeterminado que quieras
            arista_invertida = Arista(arista.nodo2, arista.nodo1, pesos=pesos_default)
            return arista in self.aristas or arista_invertida in self.aristas
   
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
        """
        Guarda el grafo en formato .dot para usar con Graphviz.
        :param filename: Nombre del archivo donde se guardará el grafo.
        """
        with open(filename, 'w') as f:
            # Escribir la cabecera del grafo (digraph para dirigido o graph para no dirigido)
            f.write("digraph G {\n" if self.dirigido else "graph G {\n")

            # Obtener todos los nodos involucrados en las aristas
            nodoArista = {arista.nodo1.id for arista in self.aristas}.union({arista.nodo2.id for arista in self.aristas})
            
            # Escribir los nodos en el archivo .dot
            for nodo_id in nodoArista:
                f.write(f'"{nodo_id}";\n')

            # Escribir las aristas y sus pesos
            for arista in self.aristas:
                peso = arista.pesos  # Obtener el peso de la arista
                distancia_redondeada = round(peso, 2)  # Redondear el peso a 2 decimales
                if self.dirigido:
                    # Grafo dirigido
                    f.write(f'    "{arista.nodo1.id}" -> "{arista.nodo2.id}" [label="{distancia_redondeada}", len="{distancia_redondeada}"];\n')
                else:
                    # Grafo no dirigido
                    f.write(f'    "{arista.nodo1.id}" -- "{arista.nodo2.id}" [label="{distancia_redondeada}", len="{distancia_redondeada}"];\n')

            # Cerrar la definición del grafo
            f.write("}\n")
    
    def dijkstra(self, nodo_inicio):
        # Inicializar distancias con infinito para todos excepto el nodo de inicio
        distancias = {nodo: float('inf') for nodo in self.nodos}
        distancias[nodo_inicio] = 0

        # Cola de prioridad para nodos a explorar, basada en la distancia
        cola_prioridad = [(0, nodo_inicio)]
        heapq.heapify(cola_prioridad)

        # Mantener un diccionario de predecesores
        predecesores = {nodo: None for nodo in self.nodos}

        while cola_prioridad:
            distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

            # Si la distancia actual es mayor que la registrada, ignorar
            if distancia_actual > distancias[nodo_actual]:
                continue

            # Explorar vecinos del nodo actual
            for vecino, peso in self.vecinos_con_peso(nodo_actual):
                nueva_distancia = distancia_actual + peso

                # Si encontramos un camino más corto hacia el vecino, lo actualizamos
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = nodo_actual
                    heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

        return distancias, predecesores

    def vecinos_con_peso(self, nodo):
        #Devuelve una lista de tuplas (vecino, peso) para cada arista que conecta con el nodo.
        if nodo not in self.nodos:
            raise ValueError("El nodo no pertenece al grafo.")

        vecinos = []
        for arista in self.aristas:
            if arista.nodo1 == nodo:
                vecinos.append((arista.nodo2, arista.pesos))
            elif arista.nodo2 == nodo:
                vecinos.append((arista.nodo1, arista.pesos))
        return vecinos

    def guardar_graphviz_con_dijkstra(self, filename, nodo_inicio):
        distancias, predecesores = self.dijkstra(nodo_inicio)
        
        with open(filename, 'w') as f:
            f.write("digraph G {\n" if self.dirigido else "graph G {\n")

            # Escribir los nodos con las distancias desde el nodo de origen
            for nodo in self.nodos:
                distancia = distancias.get(nodo, float('inf'))
                f.write(f'"{nodo.id} ({distancia:.2f})";\n')

            # Escribir solo las aristas del árbol de recorrido de Dijkstra
            for nodo in self.nodos:
                # Si el nodo tiene predecesor, escribimos la arista correspondiente
                if predecesores[nodo]:
                    predecesor = predecesores[nodo]
                    peso = self.obtener_peso_arista(predecesor, nodo)  # Método para obtener el peso
                    distancia_redondeada = round(peso, 2)
                    
                    if self.dirigido:
                        f.write(f'    "{predecesor.id} ({distancias[predecesor]:.2f})" -> "{nodo.id} ({distancias[nodo]:.2f})" [label="{distancia_redondeada}", len="{distancia_redondeada}"];\n')
                    else:
                        f.write(f'    "{predecesor.id} ({distancias[predecesor]:.2f})" -- "{nodo.id} ({distancias[nodo]:.2f})" [label="{distancia_redondeada}", len="{distancia_redondeada}"];\n')

            f.write("}\n")

    def obtener_peso_arista(self, nodo1, nodo2):
        # Busca el peso de la arista entre nodo1 y nodo2 en el grafo
        for arista in self.aristas:
            if (arista.nodo1 == nodo1 and arista.nodo2 == nodo2) or (arista.nodo1 == nodo2 and arista.nodo2 == nodo1):
                return arista.pesos
        return None  # Si no se encuentra la arista

    def mostrar_grafo(self):
        print(f"Grafo {'dirigido' if self.dirigido else 'no dirigido'} creado con {len(self.nodos)} nodos y {len(self.aristas)} aristas.")

    def grado_nodo(self, nodo):
        if nodo in self.nodos:
            return len(nodo.aristas)
        return 0
    
def grafoMalla(m, n, dirigido=False):
    """Genera un grafo de malla de tamaño m x n con pesos aleatorios en las aristas."""
    if m <= 1 or n <= 1:
        raise ValueError("Los valores de m y n deben ser mayores que 1.")

    grafo = Grafo(dirigido)
    nodos = [[Nodo(f"n{i}_{j}", valor=random.uniform(0.0, 50.0)) for j in range(n)] for i in range(m)]
    
    for i in range(m):
        for j in range(n):
            grafo.agregar_nodo(nodos[i][j])
            if i < m - 1:
                pesos = random.uniform(1.0, 10.0)  # Asignar peso aleatorio a la arista
                grafo.agregar_arista(Arista(nodos[i][j], nodos[i + 1][j], pesos))  # Cambiado a 'pesos'
            if j < n - 1:
                pesos = random.uniform(1.0, 10.0)  # Asignar peso aleatorio a la arista
                grafo.agregar_arista(Arista(nodos[i][j], nodos[i][j + 1], pesos))  # Cambiado a 'pesos'
    
    return grafo

def grafoErdosRenyi(n, m, dirigido=False):
    """Genera un grafo aleatorio según el modelo Erdös-Rényi."""
    if n <= 0:
        raise ValueError("El número de nodos debe ser mayor que 0.")
    if m < n - 1:
        raise ValueError("El número de aristas debe ser al menos n-1.")

    grafo = Grafo(dirigido)
    nodos = [Nodo(i, valor=random.uniform(0.0, 50.0)) for i in range(n)]
    
    for nodo in nodos:
        grafo.agregar_nodo(nodo)

    aristas = set()

    for i in range(n-1):
        arista = Arista(nodos[i], nodos[i+1], pesos=random.uniform(1.0, 10.0))  # Cambiado a 'pesos'
        aristas.add(arista)
        grafo.agregar_arista(arista)
    
    while len(aristas) < m:
        n1, n2 = random.sample(range(n), 2)
        if n1 == n2:
            continue

        arista = Arista(nodos[n1], nodos[n2], pesos=random.uniform(1.0, 10.0))  # Cambiado a 'pesos'
    
        if not dirigido and (arista in aristas or Arista(nodos[n2], nodos[n1], pesos=random.uniform(1.0, 10.0)) in aristas):  # Cambiado a 'pesos'
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
    nodos = [Nodo(i, valor=random.uniform(0.0, 50.0)) for i in range(n)]
    
    for nodo in nodos:
        grafo.agregar_nodo(nodo)

    for i in range(n):
        for j in range(n):
            if i != j:
                if random.random() < p:
                    pesos = random.uniform(1.0, 10.0)  # Asignamos el peso como 'pesos'
                    grafo.agregar_arista(Arista(nodos[i], nodos[j], pesos))  # Cambiado a 'pesos'

    return grafo

def grafoGeografico(n, r, dirigido=False):
    """Genera un grafo aleatorio según el modelo geográfico.""" 
    if n <= 0:
        raise ValueError("El número de nodos debe ser mayor que 0.")
    if not (0 < r <= 1):
        raise ValueError("La distancia r debe estar entre 0 y 1.")

    grafo = Grafo(dirigido)
    posiciones = [(random.random(), random.random()) for _ in range(n)]
    nodos = [Nodo(i, valor=random.uniform(0.0, 50.0)) for i in range(n)]
    
    for nodo in nodos:
        grafo.agregar_nodo(nodo)

    for i in range(n):
        for j in range(i + 1, n):
            distancia = math.sqrt((posiciones[i][0] - posiciones[j][0]) ** 2 +
                                  (posiciones[i][1] - posiciones[j][1]) ** 2)
            if distancia <= r:
                pesos = distancia  # Usamos la distancia como el peso de la arista
                grafo.agregar_arista(Arista(nodos[i], nodos[j], pesos))  # Cambiado a 'pesos'
                if not dirigido:
                    grafo.agregar_arista(Arista(nodos[j], nodos[i], pesos))  # Cambiado a 'pesos'

    return grafo

def grafoBarabasiAlbert(n, d, dirigido=False, auto=False):
    if n < 1 or d < 2:
        raise ValueError("Error: n > 0 y d > 1")
    
    grafo = Grafo(dirigido)
    nodos_deg = dict()  # Diccionario para llevar el conteo del grado de cada nodo.
    
    # Crear nodos
    for nodo_id in range(n):
        nodo = Nodo(nodo_id, valor=random.uniform(0.0, 50.0))  # Nodo con valor
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

            if p <= 1 - nodos_deg[v.id] / d and grafo.agregar(Arista(nodo, v, pesos=random.uniform(1.0, 10.0))):  # Cambiado a 'pesos'
                nodos_deg[nodo.id] += 1
                if not equal_nodes:
                    nodos_deg[v.id] += 1

    return grafo

def grafoDorogovtsevMendes(n, dirigido=False):
    """Genera un grafo según el modelo Dorogovtsev-Mendes con pesos en las aristas."""
    if n < 3:
        raise ValueError("El número de nodos debe ser al menos 3.")

    grafo = Grafo(dirigido)
    
    # Inicializa un triángulo
    nodos = [Nodo(i, valor=random.uniform(0.0, 50.0)) for i in range(3)]  # Asegurándote de pasar el valor
    for nodo in nodos:
        grafo.agregar_nodo(nodo)
    
    # Agregar las tres aristas iniciales con pesos aleatorios
    grafo.agregar_arista(Arista(nodos[0], nodos[1], pesos=random.uniform(1.0, 10.0)))
    grafo.agregar_arista(Arista(nodos[1], nodos[2], pesos=random.uniform(1.0, 10.0)))
    grafo.agregar_arista(Arista(nodos[0], nodos[2], pesos=random.uniform(1.0, 10.0)))

    # Agregar nodos adicionales
    for i in range(3, n):
        nuevo_nodo = Nodo(i, valor=random.uniform(0.0, 50.0))  # Asegurándote de pasar el valor
        grafo.agregar_nodo(nuevo_nodo)
        
        # Seleccionar una arista aleatoria existente
        arista_random = random.choice(list(grafo.aristas))  # Convertir a lista para elegir al azar
        
        # Agregar las aristas desde el nuevo nodo a los nodos de la arista seleccionada
        grafo.agregar_arista(Arista(nuevo_nodo, arista_random.nodo1, pesos=random.uniform(1.0, 10.0)))
        grafo.agregar_arista(Arista(nuevo_nodo, arista_random.nodo2, pesos=random.uniform(1.0, 10.0)))

    return grafo
