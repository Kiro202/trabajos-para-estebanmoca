# ==========================================
# DETECTOR DE ZOMBIES
# Perceptrón + Backpropagation
# ==========================================

import numpy as np
import random

# ==========================================
# DATOS DE ENTRENAMIENTO
# ==========================================
# [temperatura, agresividad, pulso, color_piel]
# Resultado:
# 0 = Humano
# 1 = Zombie

datos = np.array([
    [37, 2, 80, 1],
    [36, 3, 75, 2],
    [38, 1, 85, 1],
    [35, 4, 70, 3],

    [25, 9, 20, 9],
    [28, 8, 30, 8],
    [30, 7, 40, 7],
    [27, 10, 15, 10]
])

salidas = np.array([
    0,
    0,
    0,
    0,

    1,
    1,
    1,
    1
])

# ==========================================
# NORMALIZAR DATOS
# ==========================================

maximos = np.max(datos, axis=0)

datos = datos / maximos

# ==========================================
# PERCEPTRÓN SIMPLE
# ==========================================

class Perceptron:

    def __init__(self, entradas, tasa_aprendizaje=0.1):
        self.pesos = np.random.rand(entradas)
        self.bias = random.random()
        self.lr = tasa_aprendizaje

    def activacion(self, x):
        return 1 if x >= 0 else 0

    def predecir(self, x):
        suma = np.dot(x, self.pesos) + self.bias
        return self.activacion(suma)

    def entrenar(self, X, y, epocas=100):

        for epoca in range(epocas):

            for i in range(len(X)):

                prediccion = self.predecir(X[i])

                error = y[i] - prediccion

                self.pesos += self.lr * error * X[i]
                self.bias += self.lr * error

# ==========================================
# CREAR Y ENTRENAR PERCEPTRÓN
# ==========================================

perceptron = Perceptron(4)

perceptron.entrenar(datos, salidas)

# ==========================================
# RED NEURONAL CON BACKPROPAGATION
# ==========================================

import numpy as np

class RedNeuronal:

    def __init__(self):

        # PESOS con valores positivos y negativos
        self.pesos_entrada_oculta = np.random.uniform(-1, 1, (4, 4))
        self.pesos_oculta_salida = np.random.uniform(-1, 1, (4, 1))

        # BIAS
        self.bias_oculta = np.zeros((1, 4))
        self.bias_salida = np.zeros((1, 1))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def derivada_sigmoid(self, x):
        return x * (1 - x)

    def entrenar(self, X, y, epocas=10000, lr=0.1):

        y = y.reshape(-1, 1)

        for _ in range(epocas):

            # ---------- FORWARD ----------

            capa_oculta_entrada = (
                np.dot(X, self.pesos_entrada_oculta)
                + self.bias_oculta
            )

            capa_oculta = self.sigmoid(capa_oculta_entrada)

            salida_entrada = (
                np.dot(capa_oculta, self.pesos_oculta_salida)
                + self.bias_salida
            )

            salida = self.sigmoid(salida_entrada)

            # ---------- ERROR ----------

            error = y - salida

            # ---------- BACKPROPAGATION ----------

            ajuste_salida = (
                error * self.derivada_sigmoid(salida)
            )

            error_oculta = ajuste_salida.dot(
                self.pesos_oculta_salida.T
            )

            ajuste_oculta = (
                error_oculta *
                self.derivada_sigmoid(capa_oculta)
            )

            # ---------- ACTUALIZAR PESOS ----------

            self.pesos_oculta_salida += (
                capa_oculta.T.dot(ajuste_salida) * lr
            )

            self.bias_salida += (
                np.sum(ajuste_salida, axis=0, keepdims=True) * lr
            )

            self.pesos_entrada_oculta += (
                X.T.dot(ajuste_oculta) * lr
            )

            self.bias_oculta += (
                np.sum(ajuste_oculta, axis=0, keepdims=True) * lr
            )

    def predecir(self, x):

        capa_oculta = self.sigmoid(
            np.dot(x, self.pesos_entrada_oculta)
            + self.bias_oculta
        )

        salida = self.sigmoid(
            np.dot(capa_oculta, self.pesos_oculta_salida)
            + self.bias_salida
        )

        return salida

# ==========================================
# ENTRENAR RED NEURONAL
# ==========================================

red = RedNeuronal()

red.entrenar(datos, salidas)

# ==========================================
# PROBAR NUEVO CASO
# ==========================================

while True:

    print("\n====================================")
    print("       DETECTOR DE ZOMBIES")
    print("====================================")

    print("\n1. Probar humano de ejemplo")
    print("2. Probar zombie de ejemplo")
    print("3. Ingresar datos manualmente")
    print("4. Salir")

    opcion = input("\nSeleccione una opción: ")

    # ==========================================
    # HUMANO PREDEFINIDO
    # ==========================================

    if opcion == "1":

        temperatura = 37
        agresividad = 2
        pulso = 80
        color_piel = 1

        print("\n🟢 Humano de prueba cargado")

    # ==========================================
    # ZOMBIE PREDEFINIDO
    # ==========================================

    elif opcion == "2":

        temperatura = 25
        agresividad = 9
        pulso = 20
        color_piel = 9

        print("\n☠ Zombie de prueba cargado")

    # ==========================================
    # DATOS MANUALES
    # ==========================================

    elif opcion == "3":

        print("\nEjemplo humano:")
        print("Temperatura:37 Agresividad:2 Pulso:80 Palidez:1")

        print("\nEjemplo zombie:")
        print("Temperatura:25 Agresividad:9 Pulso:20 Palidez:9")

        temperatura = float(input("\nTemperatura corporal: "))
        agresividad = float(input("Nivel de agresividad (1-10): "))
        pulso = float(input("Pulso cardiaco: "))
        color_piel = float(input("Palidez de piel (1-10): "))

    # ==========================================
    # SALIR
    # ==========================================

    elif opcion == "4":

        print("\nSaliendo del detector...")
        break

    else:

        print("\n❌ Opción inválida")
        continue

    # ==========================================
    # CREAR CASO
    # ==========================================

    nuevo = np.array([
        temperatura,
        agresividad,
        pulso,
        color_piel
    ])

    # Normalizar
    nuevo = nuevo / maximos

    # ==========================================
    # RESULTADO PERCEPTRÓN
    # ==========================================

    resultado_perceptron = perceptron.predecir(nuevo)

    print("\n--- RESULTADO PERCEPTRÓN ---")

    if resultado_perceptron == 1:
        print("⚠ Posible Zombie")
    else:
        print("🟢 Humano detectado")

    # ==========================================
    # RESULTADO RED NEURONAL
    # ==========================================

    resultado_red = red.predecir(nuevo)

    print("\n--- RESULTADO RED NEURONAL ---")

    probabilidad = resultado_red.item() * 100

    if probabilidad >= 50:
        print(f"☠ Zombie detectado ({probabilidad:.2f}%)")
    else:
        print(f"🟢 Humano ({100 - probabilidad:.2f}%)")

    input("\nPresiona ENTER para continuar...")