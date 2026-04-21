#  Problema 1 — Greedy Real
# Contexto: Sistema de cajero automático

# Un cajero debe dispensar $87,500 COP usando billetes de [50000, 20000, 10000, 5000, 1000].

# Implementa el algoritmo greedy en Python o Java
# Muestra la traza completa paso a paso
# ¿Qué pasa si agregas un billete de $7000? ¿Sigue siendo óptimo?
# Calcula la complejidad de tu solución

# Cambio para $67 con [50,25,10,5,1] 
# monto = 67 
# monedas = [50, 25, 10, 5, 1] 
# resultado = [] 
# for moneda in monedas: 
#     while monto >= moneda:
#         resultado.append(moneda)
#         monto -= moneda 
# print (resultado)
#                               SOLUCION DEL PROBLEMA 1
monto = 87500 
billetes = [50000, 20000, 10000, 5000, 1000] 
resultado = [] 
for moneda in billetes: 
    while monto >= moneda:
        resultado.append(moneda)
        monto -= moneda 
print(resultado) #[50000,20000,10000,5000,1000,1000] 87000
# no da exacto porque no hay billetes de 500 pero asi esta bien

# 📌 Problema 2 — Huffman
# Contexto: Compresión de logs de un servidor

# Un log repite las siguientes palabras: ERROR(45), INFO(120), WARN(30), DEBUG(80), TRACE(15).

# Construye el árbol de Huffman paso a paso
# Asigna códigos binarios a cada palabra
# Calcula bits usados sin y con compresión
# ¿Qué porcentaje de espacio se ahorra?
#                          SOLUCION DEL PROBLEMA 2
import heapq

# Nodo del árbol
class Nodo:
    def __init__(self, frecuencia, simbolo=None, izquierda=None, derecha=None):
        self.frecuencia = frecuencia
        self.simbolo = simbolo
        self.izquierda = izquierda
        self.derecha = derecha

    # Para que heapq pueda comparar nodos
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia


# Construir árbol de Huffman
def construir_arbol(frecuencias):
    heap = []

    # Crear nodos hoja
    for simbolo, freq in frecuencias.items():
        heapq.heappush(heap, Nodo(freq, simbolo))

    # Construcción del árbol
    while len(heap) > 1:
        nodo1 = heapq.heappop(heap)
        nodo2 = heapq.heappop(heap)

        nuevo = Nodo(
            nodo1.frecuencia + nodo2.frecuencia,
            izquierda=nodo1,
            derecha=nodo2
        )

        heapq.heappush(heap, nuevo)

    return heap[0]


# Generar códigos
def generar_codigos(nodo, codigo_actual="", codigos={}):
    if nodo is None:
        return

    # Si es hoja
    if nodo.simbolo is not None:
        codigos[nodo.simbolo] = codigo_actual
        return

    generar_codigos(nodo.izquierda, codigo_actual + "0", codigos)
    generar_codigos(nodo.derecha, codigo_actual + "1", codigos)

    return codigos


# Calcular bits
def calcular_bits(frecuencias, codigos):
    total = 0
    for simbolo in frecuencias:
        total += frecuencias[simbolo] * len(codigos[simbolo])
    return total


# ===============================
# EJECUCIÓN
# ===============================

frecuencias = {
    "ERROR": 45,
    "INFO": 120,
    "WARN": 30,
    "DEBUG": 80,
    "TRACE": 15
}

# Construir árbol
arbol = construir_arbol(frecuencias)

# Obtener códigos
codigos = generar_codigos(arbol)
print(codigos)

print("Códigos de Huffman:")
for simbolo, codigo in codigos.items():
    print(f"{simbolo}: {codigo}")

# Bits
bits_huffman = calcular_bits(frecuencias, codigos)
bits_normal = sum(frecuencias.values()) * 3

print("\nBits sin compresión:", bits_normal)
print("Bits con Huffman:", bits_huffman)

ahorro = bits_normal - bits_huffman
porcentaje = (ahorro / bits_normal) * 100

print(f"Ahorro: {ahorro} bits ({porcentaje:.2f}%)")

# 📌 Problema 3 — Knapsack 0/1
# Contexto: Proyecto de inversión en startups

# Tienes $10M para invertir. Proyectos disponibles:

# 🏥 HealthTech
# ROI: $7M
# Costo: $3M
# 🤖 AI Startup
# ROI: $9M
# Costo: $5M
# 🌱 GreenTech
# ROI: $4M
# Costo: $2M
# 🚀 Fintech
# ROI: $6M
# Costo: $4M
# Construye y llena la tabla dp completa
# Identifica la cartera de inversión óptima
# Implementa el backtracking para hallar los proyectos elegidos

#                                   SOLUCION DEL PROBLEMA 3
def knapsack(proyectos, capacidad):
    n = len(proyectos)

    # Crear tabla DP
    dp = [[0] * (capacidad + 1) for _ in range(n + 1)]

    # Llenado
    for i in range(1, n + 1):
        nombre, costo, valor = proyectos[i - 1]
        for w in range(capacidad + 1):
            if costo <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - costo] + valor
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp


def backtracking(dp, proyectos, capacidad):
    seleccionados = []
    i = len(proyectos)
    w = capacidad

    while i > 0 and w > 0:
        if dp[i][w] != dp[i - 1][w]:
            nombre, costo, valor = proyectos[i - 1]
            seleccionados.append(nombre)
            w -= costo
        i -= 1

    return seleccionados[::-1]


# =========================

proyectos = [
    ("HealthTech", 3, 7),
    ("AI Startup", 5, 9),
    ("GreenTech", 2, 4),
    ("Fintech", 4, 6)
]

capacidad = 10

dp = knapsack(proyectos, capacidad)

print("ROI máximo:", dp[len(proyectos)][capacidad])

seleccion = backtracking(dp, proyectos, capacidad)
print("Proyectos elegidos:", seleccion)

# 📌 Problema 4 — LCS
# Contexto: Control de versiones de código fuente

# Dos versiones de un archivo de configuración:

# v1: "DEPLOY-PROD-DB-01"
# v2: "DEVELOP-DEBUG-01"

# Halla la LCS entre ambas cadenas
# Muestra la tabla dp completa
# Reconstruye la subsecuencia mediante backtracking
# ¿Qué significa esta LCS en el contexto del versionado?

#                               SOLUCION DEL PROBLEMA 4

def lcs(v1, v2):
    n = len(v1)
    m = len(v2)

    # Crear tabla DP
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Llenar la tabla
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if v1[i - 1] == v2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp


def reconstruir_lcs(dp, v1, v2):
    i = len(v1)
    j = len(v2)

    lcs = []

    while i > 0 and j > 0:
        if v1[i - 1] == v2[j - 1]:
            lcs.append(v1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(reversed(lcs))


def imprimir_tabla(dp, v1, v2):
    print("   ", "  ".join(v2))
    for i in range(len(dp)):
        if i == 0:
            print(" ", dp[i])
        else:
            print(v1[i - 1], dp[i])


# ===============================
# EJECUCIÓN
# ===============================

v1 = "DEPLOY-PROD-DB-01"
v2 = "DEVELOP-DEBUG-01"

dp = lcs(v1, v2)

print("Tabla DP:")
imprimir_tabla(dp, v1, v2)

resultado = reconstruir_lcs(dp, v1, v2)

print("\nLCS:", resultado)
print("Longitud:", len(resultado))