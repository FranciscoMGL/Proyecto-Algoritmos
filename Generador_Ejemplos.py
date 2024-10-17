from Biblioteca_grafos import grafoMalla, grafoErdosRenyi, grafoGilbert, grafoGeografico, grafoBarabasiAlbert, grafoDorogovtsevMendes

class EjemploGrafo:
    def __init__(self, nodos):
        self.nodos = nodos

    def crear_grafos(self):
        print(f"\nEjemplo con {self.nodos} nodos:")

        try:
            # Grafo Erdös-Rényi
            self.grafo_erdos = grafoErdosRenyi(self.nodos, self.nodos+5)
            print("Grafo Erdös-Rényi:")
            self.grafo_erdos.mostrar_grafo()
            self.grafo_erdos.guardar_graphviz(f"grafo_erdos_{self.nodos}.gv")

        except Exception as e:
            print(f"Error al crear Grafo Erdös-Rényi: {e}")

        try:
            # Grafo Gilbert
            self.grafo_gilbert = grafoGilbert(self.nodos, 0.2)
            print("Grafo Gilbert:")
            self.grafo_gilbert.mostrar_grafo()
            self.grafo_gilbert.guardar_graphviz(f"grafo_gilbert_{self.nodos}.gv")

        except Exception as e:
            print(f"Error al crear Grafo Gilbert: {e}")

        try:
            # Grafo Geográfico
            self.grafo_geografico = grafoGeografico(self.nodos, 0.2)
            print("Grafo Geográfico:")
            self.grafo_geografico.mostrar_grafo()
            self.grafo_geografico.guardar_graphviz(f"grafo_geografico_{self.nodos}.gv")

        except Exception as e:
            print(f"Error al crear Grafo Geográfico: {e}")

        try:
            # Grafo Barabási-Albert
            self.grafo_barabasi = grafoBarabasiAlbert(self.nodos, 2)
            print("Grafo Barabási-Albert:")
            self.grafo_barabasi.mostrar_grafo()
            self.grafo_barabasi.guardar_graphviz(f"grafo_barabasi_{self.nodos}.gv")

        except Exception as e:
            print(f"Error al crear Grafo Barabási-Albert: {e}")

        try:
            # Grafo Dorogovtsev-Mendes
            self.grafo_dorogovtsev = grafoDorogovtsevMendes(self.nodos)
            print("Grafo Dorogovtsev-Mendes:")
            self.grafo_dorogovtsev.mostrar_grafo()
            self.grafo_dorogovtsev.guardar_graphviz(f"grafo_dorogovtsev_{self.nodos}.gv")

        except Exception as e:
            print(f"Error al crear Grafo Dorogovtsev-Mendes: {e}")

def ejecutar_ejemplos():
    nodos_list = [15, 30, 100, 500]

    # Crear y guardar grafos de malla
    grafo_malla_30 = grafoMalla(5, 6)
    print("Grafo de Malla (30 nodos):")
    grafo_malla_30.mostrar_grafo()
    grafo_malla_30.guardar_graphviz("grafo_malla_30.gv")

    grafo_malla_100 = grafoMalla(20, 5)
    print("Grafo de Malla (100 nodos):")
    grafo_malla_100.mostrar_grafo()
    grafo_malla_100.guardar_graphviz("grafo_malla_100.gv")

    grafo_malla_500 = grafoMalla(25, 20)
    print("Grafo de Malla (500 nodos):")
    grafo_malla_500.mostrar_grafo()
    grafo_malla_500.guardar_graphviz("grafo_malla_500.gv")

    # Crear ejemplos de otros grafos
    for nodos in nodos_list:
        ejemplo = EjemploGrafo(nodos)
        ejemplo.crear_grafos()

if __name__ == "__main__":
    ejecutar_ejemplos()
