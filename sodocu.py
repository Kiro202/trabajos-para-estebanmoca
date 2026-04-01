import math
sudoku = [
    [5,3,0, 0,7,0, 0,0,0],
    [6,0,0, 1,9,5, 0,0,0],
    [0,9,8, 0,0,0, 0,6,0],

    [8,0,0, 0,6,0, 0,0,3],
    [4,0,0, 8,0,3, 0,0,1],
    [7,0,0, 0,2,0, 0,0,6],

    [0,6,0, 0,0,0, 2,8,0],
    [0,0,0, 4,1,9, 0,0,5],
    [0,0,0, 0,8,0, 0,7,9],
]
def comprobador_de_posicion(sudoku,numero,posicion_x,posicion_y):
    #comprobar las filas
    for posicion_fila in sudoku[posicion_y-1]: 
        if posicion_fila==numero:
            print("el numero ya se encuentra en fila")
            return
    #comprobar columnas,
    for posicion_columna in range(len(sudoku)-1):# 9 porque es el y dfel soducu
        if sudoku[posicion_columna][posicion_x-1]==numero:
            print("el numero ya se encuentra en columna")
            return
    #comprobador de cuadrantes
    cuadrante_x=math.floor((posicion_x-1)/3)
    cuadrante_y=math.floor((posicion_y-1)/3)
    for i in range(cuadrante_y*3,cuadrante_y*3+3):
        for ii in range(cuadrante_x*3,cuadrante_x*3+3):
            if sudoku[i][ii]==numero:
                print("el numero ya se encuentra en cuadrante")
                return
    print("sin nunguna coincidencia")

comprobador_de_posicion(sudoku,8,7,9)