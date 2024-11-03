import random
from CNodo import Nodo
from Biblioteca_grafos import Grafo, cargar_grafo_desde_gv

def procesar_grafo(archivo):
    try:
        # Cargar el grafo desde el archivo
        grafo = cargar_grafo_desde_gv(archivo)
        print(f"Grafo cargado: {archivo}")

        # Elegir un nodo inicial aleatorio
        nodo_inicial = random.choice(list(grafo.nodos.values()))
        print("Nodo inicial:", nodo_inicial.id)

        # Ejecutar BFS desde el nodo inicial y obtener el árbol inducido
        arbol_bfs = grafo.BFS(nodo_inicial.id)
        print(f"Nodos en el árbol inducido por BFS: {len(arbol_bfs.nodos)}")

        # Guardar el árbol inducido de BFS en un archivo
        arbol_bfs.mostrar_grafo()
        arbol_bfs.guardar_graphviz(f"{archivo[:-3]}_bfs.gv")

        # Imprimir las aristas del árbol inducido por BFS
        print("Aristas del árbol inducido por BFS:")
        if arbol_bfs.aristas:
            for arista in arbol_bfs.aristas:
                print(f"{arista.nodo1.id} -- {arista.nodo2.id}")
        else:
            print("No se encontraron aristas en el árbol inducido por BFS.")

    except Exception as e:
        print(f"Error procesando el archivo para BFS {archivo}: {e}")

    try:
        # Ejecutar DFS desde el nodo inicial y obtener el árbol inducido
        arbol_dfsi = grafo.DFS_I(nodo_inicial.id)
        print(f"Nodos en el árbol inducido por DFS: {len(arbol_dfsi.nodos)}")

        # Guardar el árbol inducido de BFS en un archivo
        arbol_dfsi.mostrar_grafo()
        arbol_dfsi.guardar_graphviz(f"{archivo[:-3]}_dfs_i.gv")

        # Imprimir las aristas del árbol inducido por BFS
        print("Aristas del árbol inducido por DFS:")
        if arbol_dfsi.aristas:
            for arista in arbol_dfsi.aristas:
                print(f"{arista.nodo1.id} -- {arista.nodo2.id}")
        else:
            print("No se encontraron aristas en el árbol inducido por DFS.")

    except Exception as e:
        print(f"Error procesando el archivo para DFS iterativo {archivo}: {e}")

    try:
        # Ejecutar DFS desde el nodo inicial y obtener el árbol inducido
        arbol_dfsr = grafo.DFS_R(nodo_inicial.id)
        print(f"Nodos en el árbol inducido por DFS: {len(arbol_dfsr.nodos)}")

        # Guardar el árbol inducido de DFS en un archivo
        arbol_dfsr.mostrar_grafo()
        arbol_dfsr.guardar_graphviz(f"{archivo[:-3]}_dfs_r.gv")

        # Imprimir las aristas del árbol inducido por DFS
        print("Aristas del árbol inducido por DFS:")
        if arbol_dfsr.aristas:
            for arista in arbol_dfsr.aristas:
                print(f"{arista.nodo1.id} -- {arista.nodo2.id}")
        else:
            print("No se encontraron aristas en el árbol inducido por DFS.")

    except ValueError as ve:
        print(f"ValueError en el archivo {archivo}: {ve}")
    except Exception as e:
        print(f"Error procesando el archivo {archivo}: {e}")

def procesar_grafo_dfs_i(archivo):
    try:
        # Cargar el grafo desde el archivo
        grafo = cargar_grafo_desde_gv(archivo)
        print(f"Grafo cargado: {archivo}")

        # Elegir un nodo inicial aleatorio
        nodo_inicial = random.choice(list(grafo.nodos.values()))
        print("Nodo inicial:", nodo_inicial.id)

        # Ejecutar DFS desde el nodo inicial y obtener el árbol inducido
        arbol_dfsi = grafo.DFS_I(nodo_inicial.id)
        print(f"Nodos en el árbol inducido por DFS: {len(arbol_dfsi.nodos)}")

        # Guardar el árbol inducido de BFS en un archivo
        arbol_dfsi.mostrar_grafo()
        arbol_dfsi.guardar_graphviz(f"{archivo[:-3]}_dfs_i.gv")

        # Imprimir las aristas del árbol inducido por BFS
        print("Aristas del árbol inducido por DFS:")
        if arbol_dfsi.aristas:
            for arista in arbol_dfsi.aristas:
                print(f"{arista.nodo1.id} -- {arista.nodo2.id}")
        else:
            print("No se encontraron aristas en el árbol inducido por DFS.")

    except Exception as e:
        print(f"Error procesando el archivo para DFS iterativo {archivo}: {e}")

def procesar_grafo_dfs_r(archivo):
    try:
        # Cargar el grafo desde el archivo
        grafo = cargar_grafo_desde_gv(archivo)
        print(f"Grafo cargado: {archivo}")

        # Imprimir nodos existentes en el grafo
        nodos_existentes = list(grafo.nodos.values())
        print("Nodos en el grafo:", [nodo.id for nodo in nodos_existentes])

        # Elegir un nodo inicial aleatorio
        nodo_inicial = random.choice(nodos_existentes)
        print("Nodo inicial:", nodo_inicial.id)

        # Verificar que el nodo inicial existe en el conjunto de nodos
        if nodo_inicial.id not in grafo.nodos:
            print(f"El nodo inicial '{nodo_inicial.id}' no existe en el grafo.")
            return  # Salir de la función si el nodo no existe

        # Ejecutar DFS desde el nodo inicial y obtener el árbol inducido
        arbol_dfsr = grafo.DFS_R(nodo_inicial.id)
        print(f"Nodos en el árbol inducido por DFS: {len(arbol_dfsr.nodos)}")

        # Guardar el árbol inducido de DFS en un archivo
        arbol_dfsr.mostrar_grafo()
        arbol_dfsr.guardar_graphviz(f"{archivo[:-3]}_dfs_r.gv")

        # Imprimir las aristas del árbol inducido por DFS
        print("Aristas del árbol inducido por DFS:")
        if arbol_dfsr.aristas:
            for arista in arbol_dfsr.aristas:
                print(f"{arista.nodo1.id} -- {arista.nodo2.id}")
        else:
            print("No se encontraron aristas en el árbol inducido por DFS.")

    except ValueError as ve:
        print(f"ValueError en el archivo {archivo}: {ve}")
    except Exception as e:
        print(f"Error procesando el archivo {archivo}: {e}")

if __name__ == "__main__":
    archivos = [
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_malla_30.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_malla_100.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_malla_500.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_erdos_30.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_erdos_100.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_erdos_500.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_gilbert_30.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_gilbert_100.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_gilbert_500.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_geografico_30.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_geografico_100.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_geografico_500.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_barabasi_30.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_barabasi_100.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_barabasi_500.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_dorogovtsev_30.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_dorogovtsev_100.gv',
        'C:/Users/Paco López/Documents/Proyecto-Algoritmos/Ejemplos Generados/grafo_dorogovtsev_500.gv'
    ]

    for archivo in archivos:
        procesar_grafo(archivo)
        #procesar_grafo_dfs_i(archivo)
        #procesar_grafo_dfs_r(archivo)
