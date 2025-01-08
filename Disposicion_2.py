from Biblioteca_grafos import grafoMalla, grafoErdosRenyi, grafoGilbert, grafoGeografico, grafoBarabasiAlbert, grafoDorogovtsevMendes
import pygame
import random
import math

class AlgoritmoFruchtermanReingold:
    def __init__(self, conjunto_nodos, conjunto_aristas, anchura=1800, altura=1000):
        self.conjunto_nodos = conjunto_nodos
        self.conjunto_aristas = conjunto_aristas
        self.anchura = anchura
        self.altura = altura

    def ejecutar(self, constante_repulsion, constante_atraccion, numero_iteraciones, constante_amortiguamiento, umbral_distanacia):
        # Colores
        color_fondo = (0, 0, 0)
        color_punto = (255, 255, 255)
        color_linea = (99, 255, 11)

        # Configuración de Pygame
        pygame.init()
        ventana_grafica = pygame.display.set_mode((self.anchura, self.altura))
        pygame.display.set_caption("Fruchterman-Reingold")
        reloj_pygame = pygame.time.Clock()

        def dibujar_grafo():
            ventana_grafica.fill(color_fondo)
            for identificador, propiedades in self.conjunto_nodos.items():
                pygame.draw.circle(ventana_grafica, color_punto, (int(propiedades['x']), int(propiedades['y'])), 8)
            for nodo1, nodo2 in self.conjunto_aristas:
                pygame.draw.line(ventana_grafica, color_linea, (int(self.conjunto_nodos[nodo1]['x']), int(self.conjunto_nodos[nodo1]['y'])),
                                 (int(self.conjunto_nodos[nodo2]['x']), int(self.conjunto_nodos[nodo2]['y'])), 1)
            pygame.display.flip()
            reloj_pygame.tick(60)

        # Bucle principal de iteraciones
        for _ in range(numero_iteraciones):
            # Reiniciar fuerzas
            for identificador in self.conjunto_nodos:
                self.conjunto_nodos[identificador]['fx'] = 0
                self.conjunto_nodos[identificador]['fy'] = 0

            # Fuerzas de repulsión
            for nodo1, propiedades1 in self.conjunto_nodos.items():
                for nodo2, propiedades2 in self.conjunto_nodos.items():
                    if nodo1 != nodo2:
                        dx = propiedades1['x'] - propiedades2['x']
                        dy = propiedades1['y'] - propiedades2['y']
                        distancia = math.sqrt(dx**2 + dy**2) or 1
                        if distancia < umbral_distanacia:
                            fuerza = constante_repulsion**2 / distancia
                            self.conjunto_nodos[nodo1]['fx'] += (dx / distancia) * fuerza
                            self.conjunto_nodos[nodo1]['fy'] += (dy / distancia) * fuerza

            # Fuerzas de atracción
            for nodo1, nodo2 in self.conjunto_aristas:
                dx = self.conjunto_nodos[nodo2]['x'] - self.conjunto_nodos[nodo1]['x']
                dy = self.conjunto_nodos[nodo2]['y'] - self.conjunto_nodos[nodo1]['y']
                distancia = math.sqrt(dx**2 + dy**2) or 1
                if distancia < umbral_distanacia:
                    fuerza = (distancia**2) / constante_atraccion
                    self.conjunto_nodos[nodo1]['fx'] += (dx / distancia) * fuerza
                    self.conjunto_nodos[nodo1]['fy'] += (dy / distancia) * fuerza
                    self.conjunto_nodos[nodo2]['fx'] -= (dx / distancia) * fuerza
                    self.conjunto_nodos[nodo2]['fy'] -= (dy / distancia) * fuerza

            # Ajuste para evitar solapamientos
            for nodo1, propiedades1 in self.conjunto_nodos.items():
                for nodo2, propiedades2 in self.conjunto_nodos.items():
                    if nodo1 != nodo2:
                        dx = propiedades1['x'] - propiedades2['x']
                        dy = propiedades1['y'] - propiedades2['y']
                        distancia = math.sqrt(dx**2 + dy**2) or 1
                        if distancia < umbral_distanacia:
                            # Separar nodos para evitar solapamiento
                            distancia_superpuesta = umbral_distanacia - distancia
                            propiedades1['x'] += (dx / distancia) * distancia_superpuesta / 2
                            propiedades1['y'] += (dy / distancia) * distancia_superpuesta / 2
                            propiedades2['x'] -= (dx / distancia) * distancia_superpuesta / 2
                            propiedades2['y'] -= (dy / distancia) * distancia_superpuesta / 2

            # Actualizar posiciones con amortiguamiento
            for nodo, propiedades in self.conjunto_nodos.items():
                fx = propiedades['fx']
                fy = propiedades['fy']
                distancia = math.sqrt(fx**2 + fy**2) or 0.01
                if distancia > constante_amortiguamiento:
                    fx = (fx / distancia) * constante_amortiguamiento
                    fy = (fy / distancia) * constante_amortiguamiento
                self.conjunto_nodos[nodo]['x'] = min(max(propiedades['x'] + fx, 0), self.anchura)
                self.conjunto_nodos[nodo]['y'] = min(max(propiedades['y'] + fy, 0), self.altura)

            # Dibujar el grafo
            dibujar_grafo()

            # Retraso de 30 ms para ralentizar la visualización
            pygame.time.delay(30)  # 30 milisegundos de retraso

        # Mantener la ventana abierta
        ejecutando = True
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
        pygame.quit()

# Ejemplo de uso
if __name__ == "__main__":
    grafo= grafoErdosRenyi(500, 666)
    # Extraer nodos y aristas del grafo
    conjunto_nodos = {nodo.id: {'x': random.randint(600, 1200), 'y': random.randint(330, 660), 'fx': 0, 'fy': 0} for nodo in grafo.nodos}
    conjunto_aristas = [(arista.nodo1.id, arista.nodo2.id) for arista in grafo.aristas]

    # Ajustar parámetros de Fruchterman-Reingold para evitar la sobreposición
    fr_algoritmo = AlgoritmoFruchtermanReingold(conjunto_nodos, conjunto_aristas)
    fr_algoritmo.ejecutar(constante_repulsion=1.0, constante_atraccion=0.3, numero_iteraciones=1000, constante_amortiguamiento=0.001, umbral_distanacia=40)
