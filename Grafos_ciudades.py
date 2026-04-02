from collections import deque
import heapq
class Grafo:
    def __init__(self, dirigido=False):
        self.lista_adyacencia = {}
        self.dirigido = dirigido

    def agregar_nodo(self, nodo):
        if nodo not in self.lista_adyacencia:
            self.lista_adyacencia[nodo] = []

    def agregar_arista(self, origen, destino, peso=1):
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self.lista_adyacencia[origen].append((destino, peso))
        if not self.dirigido:
            self.lista_adyacencia[destino].append((origen, peso))

    def mostrar(self):
        for nodo, vecinos in self.lista_adyacencia.items():
            conexiones = ', '.join(f"{v}({p})" for v, p in vecinos)
            print(f"{nodo} → [{conexiones}]")
    def get_lista_adyacencia(self):
        return self.lista_adyacencia

def bfs(grafo, inicio):
    visitados = set()
    cola = deque([inicio])
    visitados.add(inicio)
    orden = []

    while cola:
        nodo = cola.popleft()
        orden.append(nodo)

        for vecino, _ in grafo.lista_adyacencia.get(nodo, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)

    return orden
def dijkstra(grafo, inicio):
    """
    Encuentra la distancia mínima desde 'inicio'
    a todos los demás nodos del grafo ponderado.
    Complejidad: O((V + E) log V)
    """
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    heap = [(0, inicio)]  # (costo, nodo)
    predecesores = {nodo: None for nodo in grafo}

    while heap:
        costo_actual, nodo_actual = heapq.heappop(heap)

        if costo_actual > distancias[nodo_actual]:
            continue

        for vecino, peso in grafo[nodo_actual]:
            nuevo_costo = costo_actual + peso
            if nuevo_costo < distancias[vecino]:
                distancias[vecino] = nuevo_costo
                predecesores[vecino] = nodo_actual
                heapq.heappush(heap, (nuevo_costo, vecino))

    return distancias, predecesores
def reconstruir_ruta(predecesores, inicio, fin):
    ruta = []
    actual = fin
    while actual is not None:
        ruta.append(actual)
        actual = predecesores[actual]
    return ruta[::-1]
# --- Ejemplo: Red de ciudades colombianas ---
metro_bogota = Grafo()

metro = {
    "Portal Norte":   ["Toberín"],
    "Toberín":        ["Portal Norte", "Calle 142"],
    "Calle 142":      ["Toberín", "Calle 127"],
    "Calle 127":      ["Calle 142", "Pepe Sierra", "Alcalá"],
    "Pepe Sierra":    ["Calle 127", "Niza"],
    "Alcalá":         ["Calle 127", "Calle 100"],
    "Niza":           ["Pepe Sierra", "Calle 100"],
    "Calle 100":      ["Alcalá", "Niza", "Virrey"],
    "Virrey":         ["Calle 100", "Centro"],
    "Centro":         ["Virrey", "Portal Sur"],
    "Portal Sur":     ["Centro"],
}

for estacion in metro:
    for conexion in metro[estacion]:
        metro_bogota.agregar_arista(f"{estacion}",   f"{conexion}"    )

metro_bogota.mostrar()
inicio=input("donde estas?")
final=input("donde quiere ir?")
distancias, pred = dijkstra(metro_bogota.get_lista_adyacencia(), f"{inicio}")
ruta = reconstruir_ruta(pred, f"{inicio}", f"{final}")

print(f"Distancia f{inicio} → f{final}: {distancias[f'{final}']} km")
print(f"Ruta óptima: {' → '.join(ruta)}")