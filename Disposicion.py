from Biblioteca_grafos import grafoMalla, grafoErdosRenyi, grafoGilbert, grafoGeografico, grafoBarabasiAlbert, grafoDorogovtsevMendes
import pygame
import random
import math

# Configuración de Pygame
ANCHO, ALTO = 1820, 980
FPS = 60
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Visualización de Grafos - Modelo de Resortes")
reloj = pygame.time.Clock()

# Parámetros del modelo de resortes
atraccion = 0.05  # Constante de fuerza atractiva
repulsion = 50  # Constante de fuerza repulsiva
FRICCION = 0.97 # Incrementar fricción para estabilizar
MAX_VELOCIDAD = 5  # Limitar la velocidad máxima de los nodos
MIN_DISTANCIA = 5  # Evitar explosiones por nodos demasiado cercanos

# Generar grafo utilizando el modelo deseado
grafo = grafoDorogovtsevMendes(500) # Cambiar por grafoErdosRenyi, grafoGilbert, etc.

# Extraer nodos y aristas del grafo
nodos = {nodo.id: [random.randint(10, ANCHO - 10), random.randint(10, ALTO - 10)] for nodo in grafo.nodos}
aristas = [(arista.nodo1.id, arista.nodo2.id) for arista in grafo.aristas]

# Función para calcular distancia entre dos nodos
def distancia(nodo1, nodo2):
    dx, dy = nodo2[0] - nodo1[0], nodo2[1] - nodo1[1]
    dist = math.sqrt(dx**2 + dy**2)
    return dist, dx, dy

# Simulación de fuerzas
velocidades = {i: [0, 0] for i in nodos}

# Bucle principal
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Inicializar fuerzas
    fuerzas = {i: [0, 0] for i in nodos}

    # Fuerzas atractivas (Hooke)
    for nodo1, nodo2 in aristas:
        dist, dx, dy = distancia(nodos[nodo1], nodos[nodo2])
        if dist > 0:
            fuerza = atraccion * math.log(dist + 1)
            fuerzas[nodo1][0] += fuerza * dx / dist
            fuerzas[nodo1][1] += fuerza * dy / dist
            fuerzas[nodo2][0] -= fuerza * dx / dist
            fuerzas[nodo2][1] -= fuerza * dy / dist

    # Fuerzas repulsivas (Ley de Coulomb)
    for i in nodos:
        for j in nodos:
            if i != j:
                dist, dx, dy = distancia(nodos[i], nodos[j])
                if dist > MIN_DISTANCIA:
                    fuerza = repulsion / (dist**2)
                    fuerzas[i][0] -= fuerza * dx / dist
                    fuerzas[i][1] -= fuerza * dy / dist

    # Actualización de posiciones
    for i in nodos:
        velocidades[i][0] = max(-MAX_VELOCIDAD, min(MAX_VELOCIDAD, (velocidades[i][0] + fuerzas[i][0]) * FRICCION))
        velocidades[i][1] = max(-MAX_VELOCIDAD, min(MAX_VELOCIDAD, (velocidades[i][1] + fuerzas[i][1]) * FRICCION))
        nodos[i][0] += velocidades[i][0]
        nodos[i][1] += velocidades[i][1]

    # Dibujar en Pygame
    pantalla.fill((255, 255, 255))
    for nodo1, nodo2 in aristas:
        pygame.draw.line(pantalla, (200, 200, 200), nodos[nodo1], nodos[nodo2], 1)
    for i in nodos:
        pygame.draw.circle(pantalla, (0, 0, 255), (int(nodos[i][0]), int(nodos[i][1])), 5)
    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()