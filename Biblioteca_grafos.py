from CNodo import Nodo
from CArista import Arista
from CDisjunto import Disjunto
from collections import deque
import copy
import heapq
import random
import math
class Nodo:
    def __init__(self, id, valor):
        self.id = id
        self.aristas = []
        self.valor = valor
        self.atributos = []  # Lista de atributos
    
    def __repr__(self):
        return f"Nodo(id={self.id}, aristas={len(self.aristas)}, atributos={self.atributos})"
    
    def __eq__(self,other):
        if isinstance(other, Nodo):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash(self.id)
    
class Arista:
    def __init__(self, nodo1, nodo2, pesos):  
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.pesos = pesos  # Guardamos el peso aquí
        self.atributos = []  # Lista de atributos

    def __repr__(self):
        return f"Arista({self.nodo1.id}, {self.nodo2.id}, {self.pesos})"
    
    def __eq__(self, otra_arista):
        # Definimos cómo comparar dos aristas (por nodo1, nodo2 y peso)
        return (self.nodo1 == otra_arista.nodo1 and 
                self.nodo2 == otra_arista.nodo2 and 
                self.pesos == otra_arista.pesos)
    
    def __hash__(self):
        # Necesitamos un hash para las aristas, esto es importante para cuando se usan en sets
        return hash(frozenset([self.nodo1.id, self.nodo2.id]))
class Grafo:
    def __init__(self, dirigido=False):
        self.nodos = []
        self.aristas = []
        self.dirigido = dirigido
        self.atributos = []  # Lista de atributos

    def agregar_nodo(self, nodo):
        if nodo not in self.nodos:
            self.nodos.append(nodo)

    def existe_arista(self, arista):
        """ Verifica si existe una arista en el grafo (considerando que el grafo puede ser dirigido o no). """
        if self.dirigido:
            return arista in self.aristas
        else:
            pesos_default = 1.0
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
            self.aristas.append(arista)  # Añadir directamente al conjunto

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

    def bfs(self, nodo_inicio):
        """Implementación del algoritmo de búsqueda en anchura (BFS)"""
        # Verificamos si el nodo de inicio está en el grafo
        if nodo_inicio not in self.nodos:
            raise ValueError("El nodo de inicio no existe en el grafo.")
        
        # Inicialización
        visitados = set()  # Conjunto para llevar el registro de nodos visitados
        cola = deque([nodo_inicio])  # Cola para los nodos a explorar
        orden_bfs = []  # Lista para almacenar el orden de los nodos visitados
        
        visitados.add(nodo_inicio)  # Marcamos el nodo de inicio como visitado

        while cola:
            nodo_actual = cola.popleft()  # Tomamos el siguiente nodo de la cola
            orden_bfs.append(nodo_actual)  # Agregamos el nodo actual a la lista de visitados

            # Obtenemos los vecinos del nodo actual
            for vecino, _ in self.vecinos_con_peso(nodo_actual):
                if vecino not in visitados:
                    visitados.add(vecino)  # Marcamos al vecino como visitado
                    cola.append(vecino)  # Lo agregamos a la cola para explorarlo después

        return orden_bfs

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
    
    def KruskalD(self):
        # Ordenar las aristas por peso (de menor a mayor)
        aristas_ordenadas = sorted(self.aristas, key=lambda arista: arista.pesos)
        conjunto = Disjunto()

        # Inicializar los conjuntos disjuntos
        for nodo in self.nodos:
            conjunto.conjunto(nodo)
        peso_total = 0
        aem = []

        # Iterar sobre las aristas ordenadas
        for arista in aristas_ordenadas:
            nodo1 = arista.nodo1
            nodo2 = arista.nodo2

            # Si no forman un ciclo, agregar la arista al MST
            if conjunto.explorar(nodo1) != conjunto.explorar(nodo2):
                conjunto.union(nodo1, nodo2)
                aem.append(arista)
                peso_total += arista.pesos

        print(f"Valor del arbol de expansion minima por Kruskal es: {round(peso_total,2)}")
        return aem
    
    def KruskalI(self):
        # Crear una copia del grafo para no modificar el original
        grafo_copia = copy.deepcopy(self)
        aem = []  # Usamos una lista para almacenar las aristas del AEM
        peso_total = 0
        # Ordenar las aristas por peso de forma descendente
        aristas_ordenadas = sorted(self.aristas, key=lambda arista: arista.pesos, reverse=True)
        
        # Iterar sobre las aristas ordenadas
        for arista in aristas_ordenadas:
            # Eliminar la arista de la copia del grafo
            grafo_copia.aristas = [a for a in grafo_copia.aristas if a != arista]
            
            # Verificar si el grafo sigue conectado usando BFS o DFS
            nodos_alcanzados = grafo_copia.bfs(grafo_copia.nodos[0])

            # Si el grafo sigue conectado (todos los nodos alcanzados), no agregar la arista
            if len(nodos_alcanzados) == len(self.nodos):
                # Si el grafo sigue conectado, significa que la arista no es esencial para la conectividad
                #print(f"Arista {arista.nodo1}-{arista.nodo2} no agregada al AEM porque el grafo sigue conectado")
                continue
            else:
                # Si no sigue conectado, agregarla al AEM (porque es esencial para mantener la conectividad)
                #print(f"Arista {arista.nodo1}-{arista.nodo2} agregada al AEM")
                aem.append(arista)  # Agregar la arista al AEM
                peso_total += arista.pesos
                # Si el grafo se desconectó, debemos volver a insertar la arista para no romper la conectividad
                grafo_copia.agregar_arista(arista)

        # Imprimir el AEM final para depuración
        #print("AEM final:")
        #for arista in aem:
            #print(f"Nodos: {arista.nodo1}, {arista.nodo2}, Peso: {arista.pesos}")
        print(f"Valor del arbol de expansion minima por Kruskal Inverso es: {round(peso_total,2)}")
        return aem
    
    def Prim(self):
        # Elegir un nodo inicial aleatorio
        nodo_inicio = random.choice(list(self.nodos))
        #print(f"Nodo inicial seleccionado: {nodo_inicio}")

        # Inicializar estructuras
        visitados = set()
        aem = []  # Lista de aristas del Árbol de Expansión Mínima
        cola_prioridad = []
        peso_total = 0
        # Añadir las aristas del nodo inicial al heap
        for vecino, peso in self.vecinos_con_peso(nodo_inicio):
            heapq.heappush(cola_prioridad, (peso, nodo_inicio, vecino))

        visitados.add(nodo_inicio)

        # Construir el MST
        while cola_prioridad:
            peso, origen, destino = heapq.heappop(cola_prioridad)

            # Ignorar si el nodo destino ya fue visitado
            if destino in visitados:
                continue

            # Añadir la arista al MST
            aem.append((origen, destino, peso))
            peso_total += peso
            visitados.add(destino)

            # Añadir las aristas del nuevo nodo al heap
            for vecino, peso in self.vecinos_con_peso(destino):
                if vecino not in visitados:
                    heapq.heappush(cola_prioridad, (peso, destino, vecino))

        print(f"Valor del arbol de expansion minima por Prim es: {round(peso_total,2)}")
        return aem

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
    
    def guardar_graphviz_algoritmo(self, archivo, aem, algoritmo):
        if algoritmo == "prim":
            with open(archivo, 'w') as f:
                f.write("graph G {\n")  # Definir un grafo no dirigido

                # Recopilar nodos únicos
                nodos = set()
                for arista in aem:
                    nodo1, nodo2, peso = arista  # Desempaquetar la tupla
                    nodos.add(nodo1)
                    nodos.add(nodo2)

                # Escribir los nodos en el archivo, ordenados por su ID
                for nodo in sorted(nodos, key=lambda x: x.id):  # Ordenar nodos por atributo 'id'
                    f.write(f'  "{nodo.id}";\n')  # Usar el atributo 'id' para imprimir

                # Escribir las aristas con sus etiquetas y pesos
                for arista in aem:
                    nodo1, nodo2, peso = arista  # Desempaquetar la tupla
                    f.write(f'  "{nodo1.id}" -- "{nodo2.id}" [label="{round(peso, 2)}"];\n')

                f.write("}\n")  # Cerrar la definición del grafo
        else:
            with open(archivo, 'w') as f:
                f.write("graph G {\n")  # Esto es para grafos no dirigidos
                # Agregar los nodos al archivo
                nodos = set()  # Usamos un set para evitar nodos duplicados
                for arista in aem:
                    nodos.add(arista.nodo1.id)
                    nodos.add(arista.nodo2.id)

                # Escribir los nodos en el archivo
                for nodo in nodos:
                    f.write(f'  "{nodo}";\n')  # Asegurarse de que los nombres de los nodos estén entre comillas

                # Escribir las aristas del AEM en formato Graphviz
                for arista in aem:
                    nodo1 = arista.nodo1.id  # Suponiendo que cada nodo tiene un identificador único
                    nodo2 = arista.nodo2.id
                    peso = arista.pesos
                    # Escribir las aristas con sus etiquetas y longitud
                    f.write(f'  "{nodo1}" -- "{nodo2}" [label="{round(peso, 2)}"];\n')

                f.write("}\n")  # Cerrar la definición del grafo

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
        for nodo in self.nodos:
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
                pesos = distancia 
                grafo.agregar_arista(Arista(nodos[i], nodos[j], pesos))
                if not dirigido:
                    grafo.agregar_arista(Arista(nodos[j], nodos[i], pesos))
    return grafo

def grafoBarabasiAlbert(n, d, dirigido=False, auto=False): 
    if n < 1 or d < 2: 
        raise ValueError("Error: n > 0 y d > 1") 
    grafo = Grafo(dirigido) 
    grado_nodo = dict() 
    for nodo_id in range(n): 
        nodo = Nodo(nodo_id, valor=random.uniform(0.0, 50.0)) 
        grafo.agregar_nodo(nodo) 
        grado_nodo[nodo_id] = 0 
        
    nodos = grafo.nodos 
    
    for nodo in nodos: 
        for v in nodos: 
            if grado_nodo[nodo.id] == d: 
                break 
            if grado_nodo[v.id] == d: 
                continue 
            p = random.random() 
            if v == nodo and not auto: 
                continue 
            if p <= 1 - grado_nodo[v.id] / d and len([a for a in grafo.aristas if a.nodo1 == nodo and a.nodo2 == v]) == 0: 
                arista = Arista(nodo, v, pesos=random.uniform(1.0, 10.0)) 
                grafo.agregar_arista(arista) 
                grado_nodo[nodo.id] += 1 
                if nodo != v: 
                    grado_nodo[v.id] += 1 

    return grafo

def grafoDorogovtsevMendes(n, dirigido=False):
    """Genera un grafo según el modelo Dorogovtsev-Mendes con pesos en las aristas."""
    if n < 3:
        raise ValueError("El número de nodos debe ser al menos 3.")

    grafo = Grafo(dirigido)
    
    # Inicializa un triángulo
    nodos = [Nodo(i, valor=random.uniform(0.0, 50.0)) for i in range(3)] 
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
