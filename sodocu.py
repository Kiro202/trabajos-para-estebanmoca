import math
#paso uno definir dominio, restriciones y variables
#variables= Celdas vacias
#dominio= 1,2,3,4,5,6,7,8,9
#restriciones= sin numeros repedis por fila, columna y cuadrante

import math

class Suduku:
    def __init__(self, sudoku, contador=0,ac=0):
        self.sudoku = sudoku
        self.contador = contador
        self.ac=ac

    def mostrar_tablero(self):
        for filas in self.sudoku:
            print(filas)
        print(f"receunto de recursividad usada en este proceso: {self.contador}")

    def mostrar_tablero_con_pausas(self):
        for filas in self.sudoku:
            print(filas)
        print(f"receunto de recursividad usada en este proceso: {self.contador}")
        input("Enter para continuar: ")

    def Comprobador_de_restricciones(self, x, y, numero):
        for numero_en_fila in self.sudoku[y]:
            if numero_en_fila == numero:
                return False

        for fila in range(len(self.sudoku)):
            if self.sudoku[fila][x] == numero:
                return False

        cuadrante_x = (x // 3) * 3
        cuadrante_y = (y // 3) * 3

        for i in range(cuadrante_y, cuadrante_y + 3):
            for j in range(cuadrante_x, cuadrante_x + 3):
                if self.sudoku[i][j] == numero:
                    return False

        return True

    def Bc_simple(self, pausas=False):
        self.contador=self.contador+1
        for y in range(9):
            for x in range(9):
                if self.sudoku[y][x] == 0:
                    for numero in range(1, 10):
                        if self.Comprobador_de_restricciones(x, y, numero):
                            self.sudoku[y][x] = numero
                            if pausas:
                                self.mostrar_tablero_con_pausas()
                            if self.Bc_simple(pausas):
                                return True
                            self.sudoku[y][x] = 0
                    return False
        return True
    #hasta aqui va lo sentillo

    def comprobador_de_posibles_dominios(self, x, y):
        dominios = []
        for numero in range(1, 10):
            if self.Comprobador_de_restricciones(x, y, numero):
                dominios.append(numero)
        return dominios

    def Ubicaciones_celdas_vacias_con_posibilidades(self):
        celdas_vacias = {}
        for y in range(9):
            for x in range(9):
                if self.sudoku[y][x] == 0:
                    celdas_vacias[(x, y)] = self.comprobador_de_posibles_dominios(x, y)
        return celdas_vacias

    def ordenar_celdas_vasias_por_porsivilidades(self, celdas):
        puestos = []
        for (x, y), posibilidades in celdas.items():
            puestos.append([y, x, posibilidades])

        puestos.sort(key=lambda celda: len(celda[2]))
        return puestos

    def Bc_intermedio(self, pausas=False):
        celdas_vacias = self.Ubicaciones_celdas_vacias_con_posibilidades()
        celdas_vacias_ordenadas = self.ordenar_celdas_vasias_por_porsivilidades(celdas_vacias)

        def backtracking(celdas):
            if not celdas:
                return True
            self.contador=self.contador+1
            celda = celdas[0]
            y = celda[0]
            x = celda[1]
            posibilidades = celda[2]

            for numero in posibilidades:
                if self.Comprobador_de_restricciones(x, y, numero):
                    self.sudoku[y][x] = numero

                    if pausas:
                        print(f"{x},{y} -> {numero}")
                        self.mostrar_tablero_con_pausas()

                    if backtracking(celdas[1:]):
                        return True

                    self.sudoku[y][x] = 0

            return False

        return backtracking(celdas_vacias_ordenadas)
    #ahora el nivel mas dificil
    def Bv_dificil(self,pausas=False):
        celdas_vacias = self.Ubicaciones_celdas_vacias_con_posibilidades()
        celdas_vacias_ordenadas = self.ordenar_celdas_vasias_por_porsivilidades(celdas_vacias)
        celds_vacias_limpias=self.ac_3(celdas_vacias_ordenadas)
        if celds_vacias_limpias is None:
            return False
        def backtracking(celdas):
            if not celdas:
                return True
            self.contador=self.contador+1
            celda = celdas[0]
            y = celda[0]
            x = celda[1]
            posibilidades = celda[2]

            for numero in posibilidades:
                if self.Comprobador_de_restricciones(x, y, numero):
                    self.sudoku[y][x] = numero

                    if pausas:
                        print(f"{x},{y} -> {numero}")
                        self.mostrar_tablero_con_pausas()

                    if backtracking(celdas[1:]):
                        return True

                    self.sudoku[y][x] = 0

            return False

        return backtracking(celds_vacias_limpias)
    #Ac_3 significa que si, un elemento cambio, podemos descaras las posibilidades del resto de una vez, y si solo 
    # hay un elemento pues este elemento sera escojido... hay varios nivel de complejidad que podria uno usar... pero
    #aqui somos machos y son las 10 de la noche... voy a elejir el peor y mas dificil y luego me hecho un lolsito

    def ac_3(self, celdas):
        cambio = True

        while cambio:
            cambio = False

            for elemento in celdas:
                if len(elemento[2]) == 1:
                    valor = elemento[2][0]
                    y, x = elemento[0], elemento[1]

                    self.sudoku[y][x] = valor

                    for vecino in celdas:
                        if vecino == elemento:
                            continue

                        vy, vx = vecino[0], vecino[1]

                        if (vy == y or vx == x or 
                            ((vy // 3 == y // 3) and (vx // 3 == x // 3))):

                            if valor in vecino[2]:
                                vecino[2].remove(valor)
                                cambio = True
                                self.ac=self.ac+1

                                if len(vecino[2]) == 0:
                                    return None
        print(f"ac3 limpio {self.ac} celdas")
        return celdas    
def copiar_tablero(tablero):
    return [fila[:] for fila in tablero]                  
    


ejemplo= [
    [5,3,0, 0,7,0, 0,0,0],
    [6,0,0, 1,9,5, 0,0,0],
    [0,9,8, 0,0,0, 0,6,0],

    [8,0,0, 0,6,0, 0,0,3],
    [4,0,0, 8,0,3, 0,0,1],
    [7,0,0, 0,2,0, 0,0,6],

    [0,6,0, 0,0,0, 2,8,0],
    [0,0,0, 4,1,9, 0,0,5],
    [0,0,0, 0,8,0, 0,7,9]]
sudoku_dificil = [
    [0,0,0, 0,0,0, 0,1,2],
    [0,0,0, 0,3,5, 0,0,0],
    [0,0,0, 7,0,0, 0,0,0],

    [0,0,0, 0,0,0, 3,0,0],
    [0,0,1, 0,8,0, 5,0,0],
    [0,0,9, 0,0,0, 0,0,0],

    [0,0,0, 0,0,9, 0,0,0],
    [0,0,0, 1,2,0, 0,0,0],
    [8,4,0, 0,0,0, 0,0,0]
]
sudoku_muy_dificil = [
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,3, 0,8,5],
    [0,0,1, 0,2,0, 0,0,0],

    [0,0,0, 5,0,7, 0,0,0],
    [0,0,4, 0,0,0, 1,0,0],
    [0,9,0, 0,0,0, 0,0,0],

    [5,0,0, 0,0,0, 0,7,3],
    [0,0,2, 0,1,0, 0,0,0],
    [0,0,0, 0,4,0, 0,0,9]
]
sudoku_infernal = [
    [0,0,0, 0,0,0, 0,0,1],
    [4,0,0, 0,0,0, 0,0,0],
    [0,2,0, 0,0,0, 0,0,0],

    [0,0,0, 0,5,0, 4,0,7],
    [0,0,8, 0,0,0, 3,0,0],
    [0,0,1, 0,9,0, 0,0,0],

    [3,0,0, 4,0,0, 2,0,0],
    [0,5,0, 1,0,0, 0,0,0],
    [0,0,0, 8,0,6, 0,0,0]
]
def menu():
    while True:
        print("\n===== SOLVER SUDOKU =====")
        print("1. Resolver con Backtracking Simple")
        print("2. Resolver con MRV (Intermedio)")
        print("3. Resolver con AC-3 + Backtracking (Difícil)")
        print("4. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            print("\n--- Modo Simple ---")
            sudoku = copiar_tablero(ejemplo)
            pollo = Suduku(sudoku)

            if pollo.Bc_simple():
                pollo.mostrar_tablero()
            else:
                print("No tiene solución")

        elif opcion == "2":
            print("\n--- Modo Intermedio (MRV) ---")
            sudoku = copiar_tablero(ejemplo)
            pollo = Suduku(sudoku)

            if pollo.Bc_intermedio():
                pollo.mostrar_tablero()
            else:
                print("No tiene solución")

        elif opcion == "3":
            print("\n--- Modo Difícil (AC-3 + Backtracking) ---")
            sudoku = copiar_tablero(ejemplo)
            pollo = Suduku(sudoku)

            if pollo.Bv_dificil():
                pollo.mostrar_tablero()
            else:
                pollo.mostrar_tablero()

        elif opcion == "4":
            print("Saliendo...")
            break

        else:
            print("Opción inválida, intenta de nuevo")
menu()