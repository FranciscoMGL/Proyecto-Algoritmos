from Biblioteca_grafos import grafoMalla, grafoErdosRenyi, grafoGilbert, grafoGeografico, grafoBarabasiAlbert, grafoDorogovtsevMendes
import random

class EjemploGrafo:
    def __init__(self, nodos):
        self.nodos = nodos

    def crear_grafos(self):
        print(f"\nEjemplo con {self.nodos} nodos:")
        
        try:
            # Grafo Erdös-Rényi
            self.grafo_erdos = grafoErdosRenyi(self.nodos, self.nodos + int(self.nodos / 3))
            print("Grafo Erdös-Rényi:")
            self.grafo_erdos.mostrar_grafo()
            self.grafo_erdos.guardar_graphviz(f"grafo_erdos_{self.nodos}.gv")
            aem_kruskalD = self.grafo_erdos.KruskalD()
            self.grafo_erdos.guardar_graphviz_algoritmo(f"KruskalD_erdos_{self.nodos}.gv", aem_kruskalD, algoritmo="kruskal")
            aem_kruskalI = self.grafo_erdos.KruskalI()
            self.grafo_erdos.guardar_graphviz_algoritmo(f"KruskalI_erdos_{self.nodos}.gv", aem_kruskalI, algoritmo = "kruskal")
            aem_prim = self.grafo_erdos.Prim()
            self.grafo_erdos.guardar_graphviz_algoritmo(f"Prim_erdos_{self.nodos}.gv", aem_prim, algoritmo = "prim")

        except Exception as e:
            print(f"Error al crear Grafo Erdös-Rényi: {e}")
        
        try:
            # Grafo Gilbert
            self.grafo_gilbert = grafoGilbert(self.nodos, 0.2)
            print("Grafo Gilbert:")
            self.grafo_gilbert.mostrar_grafo()
            self.grafo_gilbert.guardar_graphviz(f"grafo_gilbert_{self.nodos}.gv")
            aem_kruskalD = self.grafo_gilbert.KruskalD()
            self.grafo_gilbert.guardar_graphviz_algoritmo(f"KruskalD_gilbert_{self.nodos}.gv", aem_kruskalD, algoritmo="kruskal")
            aem_kruskalI = self.grafo_gilbert.KruskalI()
            self.grafo_gilbert.guardar_graphviz_algoritmo(f"KruskalI_gilbert_{self.nodos}.gv", aem_kruskalI, algoritmo = "kruskal")
            aem_prim = self.grafo_gilbert.Prim()
            self.grafo_gilbert.guardar_graphviz_algoritmo(f"Prim_gilbert_{self.nodos}.gv", aem_prim, algoritmo = "prim")

        except Exception as e:
            print(f"Error al crear Grafo Gilbert: {e}")
        
        try:
            # Grafo Geográfico
            self.grafo_geografico = grafoGeografico(self.nodos, 0.5)
            print("Grafo Geográfico:")
            self.grafo_geografico.mostrar_grafo()
            self.grafo_geografico.guardar_graphviz(f"grafo_geografico_{self.nodos}.gv")
            aem_kruskalD = self.grafo_geografico.KruskalD()
            self.grafo_geografico.guardar_graphviz_algoritmo(f"KruskalD_geografico_{self.nodos}.gv", aem_kruskalD, algoritmo="kruskal")
            aem_kruskalI = self.grafo_geografico.KruskalI()
            self.grafo_geografico.guardar_graphviz_algoritmo(f"KruskalI_geografico_{self.nodos}.gv", aem_kruskalI, algoritmo = "kruskal")
            aem_prim = self.grafo_geografico.Prim()
            self.grafo_geografico.guardar_graphviz_algoritmo(f"Prim_geografico_{self.nodos}.gv", aem_prim, algoritmo = "prim")

        except Exception as e:
            print(f"Error al crear Grafo Geográfico: {e}")
        
        try:
            # Grafo Barabási-Albert
            self.grafo_barabasi = grafoBarabasiAlbert(self.nodos, 6)
            print("Grafo Barabási-Albert:")
            self.grafo_barabasi.mostrar_grafo()
            self.grafo_barabasi.guardar_graphviz(f"grafo_barabasi_{self.nodos}.gv")
            aem_kruskalD = self.grafo_barabasi.KruskalD()
            self.grafo_barabasi.guardar_graphviz_algoritmo(f"KruskalD_barabasi_{self.nodos}.gv", aem_kruskalD, algoritmo="kruskal")
            aem_kruskalI = self.grafo_barabasi.KruskalI()
            self.grafo_barabasi.guardar_graphviz_algoritmo(f"KruskalI_barabasi_{self.nodos}.gv", aem_kruskalI, algoritmo = "kruskal")
            aem_prim = self.grafo_barabasi.Prim()
            self.grafo_barabasi.guardar_graphviz_algoritmo(f"Prim_barabasi_{self.nodos}.gv", aem_prim, algoritmo = "prim")
            
        except Exception as e:
            print(f"Error al crear Grafo Barabási-Albert: {e}")
        
        try:
            # Grafo Dorogovtsev-Mendes
            self.grafo_dorogovtsev = grafoDorogovtsevMendes(self.nodos)
            print("Grafo Dorogovtsev-Mendes:")
            self.grafo_dorogovtsev.mostrar_grafo()
            self.grafo_dorogovtsev.guardar_graphviz(f"grafo_dorogovtsev_{self.nodos}.gv")
            aem_kruskalD = self.grafo_dorogovtsev.KruskalD()
            self.grafo_dorogovtsev.guardar_graphviz_algoritmo(f"KruskalD_erdos_{self.nodos}.gv", aem_kruskalD, algoritmo="kruskal")
            aem_kruskalI = self.grafo_dorogovtsev.KruskalI()
            self.grafo_dorogovtsev.guardar_graphviz_algoritmo(f"KruskalI_erdos_{self.nodos}.gv", aem_kruskalI, algoritmo = "kruskal")
            aem_prim = self.grafo_dorogovtsev.Prim()
            self.grafo_dorogovtsev.guardar_graphviz_algoritmo(f"Prim_erdos_{self.nodos}.gv", aem_prim, algoritmo = "prim")

        except Exception as e:
            print(f"Error al crear Grafo Dorogovtsev-Mendes: {e}")
        
def ejecutar_ejemplos():
    nodos_list = [30, 100]
    
    grafo_malla_30 = grafoMalla(6, 5)
    print("Grafo de Malla (30 nodos):")
    grafo_malla_30.mostrar_grafo()
    grafo_malla_30.guardar_graphviz("grafo_malla_30.gv")
    aem_kruskalD = grafo_malla_30.KruskalD()
    grafo_malla_30.guardar_graphviz_algoritmo("KruskalD_malla_30.gv", aem_kruskalD, algoritmo="kruskal")
    aem_kruskalI = grafo_malla_30.KruskalI()
    grafo_malla_30.guardar_graphviz_algoritmo("KruskalI_malla_30.gv", aem_kruskalI, algoritmo = "kruskal")
    aem_prim = grafo_malla_30.Prim()
    grafo_malla_30.guardar_graphviz_algoritmo("Prim_malla_30.gv", aem_prim, algoritmo = "prim")
    
    grafo_malla_100 = grafoMalla(10, 10)
    print("Grafo de Malla (100 nodos):")
    grafo_malla_100.mostrar_grafo()
    grafo_malla_100.guardar_graphviz("grafo_malla_100.gv")
    aem_kruskalD = grafo_malla_100.KruskalD()
    grafo_malla_100.guardar_graphviz_algoritmo("KruskalD_malla_100.gv", aem_kruskalD, algoritmo="kruskal")
    aem_kruskalI = grafo_malla_100.KruskalI()
    grafo_malla_100.guardar_graphviz_algoritmo("KruskalI_malla_100.gv", aem_kruskalI, algoritmo = "kruskal")
    aem_prim = grafo_malla_100.Prim()
    grafo_malla_100.guardar_graphviz_algoritmo("Prim_malla_100.gv", aem_prim, algoritmo = "prim")
    """
    grafo_malla_500 = grafoMalla(25, 20)
    print("Grafo de Malla (500 nodos):")
    grafo_malla_500.mostrar_grafo()
    grafo_malla_500.guardar_graphviz("grafo_malla_500.gv")
    aem_kruskalD = grafo_malla_500.KruskalD()
    grafo_malla_500.guardar_graphviz_algoritmo("KruskalD_malla_500.gv", aem_kruskalD, algoritmo="kruskal")
    aem_kruskalI = grafo_malla_500.KruskalI()
    grafo_malla_500.guardar_graphviz_algoritmo("KruskalI_malla_500.gv", aem_kruskalI, algoritmo = "kruskal")
    aem_prim = grafo_malla_500.Prim()
    grafo_malla_500.guardar_graphviz_algoritmo("Prim_malla_500.gv", aem_prim, algoritmo = "prim")
    """
    # Crear ejemplos de otros grafos
    for nodos in nodos_list:
        ejemplo = EjemploGrafo(nodos)
        ejemplo.crear_grafos()
       
if __name__ == "__main__":
    ejecutar_ejemplos()
