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
] #varios ejemplos de sudoku a resolver
sudoku2 = [
    [0,6,0, 1,0,4, 0,5,0],
    [0,0,8, 3,0,5, 6,0,0],
    [2,0,0, 0,0,0, 0,0,1],

    [8,0,0, 4,0,7, 0,0,6],
    [0,0,6, 0,0,0, 3,0,0],
    [7,0,0, 9,0,1, 0,0,4],

    [5,0,0, 0,0,0, 0,0,2],
    [0,0,7, 2,0,6, 9,0,0],
    [0,4,0, 5,0,8, 0,7,0],
]
def comprobador_de_posicion(sudoku,numero,posicion_x,posicion_y):
    #comprobar las filas
    for posicion_fila in sudoku[posicion_y-1]: 
        if posicion_fila==numero:
            print(f"el numero {numero} ya se encuentra en fila")
            return False
    #comprobar columnas,
    for posicion_columna in range(len(sudoku)):# 9 porque es el y dfel soducu
        if sudoku[posicion_columna][posicion_x-1]==numero:
            print(f"el numero {numero} ya se encuentra en columna")
            return False
    #comprobador de cuadrantes
    cuadrante_x=math.floor((posicion_x-1)/3)
    cuadrante_y=math.floor((posicion_y-1)/3)
    for i in range(cuadrante_y*3,cuadrante_y*3+3):
        for ii in range(cuadrante_x*3,cuadrante_x*3+3):
            if sudoku[i][ii]==numero:
                print(f"el numero {numero} ya se encuentra en cuadrante")
                return False
    print(f"sin nunguna coincidencia {numero}")
    return True
def organizador_de_repeticion(sudoku,y,x):
    try: 
        if len(sudoku[y][x]):
            sudoku[y][x]=0
    except:
        None
def mostrar_pantalla(sudoku,contador):
    for fila in sudoku:
        print(fila)
    input(f"numero de vuletas: {contador}\nEnter para la siguiente vuelta")
def tecnica_tanteo(sudoku,contador=1,repetir=False): #cuenta todas las posibiliades en una posicion si solo queda una entonces la pone
    for posicion_y in range(0,len(sudoku)): #hacemos que pase por todas las filas y columnas
        for posicion_x in range(0,len(sudoku)):
            if sudoku[posicion_y][posicion_x]==0: #buscamos un espacio vacio
                sudoku[posicion_y][posicion_x]=[] #lo combertimos en una lista vacia, 
                #para meter todas las probabilidades
                for numero in range(1,10): #comprobamos todos los numero
                    if comprobador_de_posicion(sudoku,numero,posicion_x+1,posicion_y+1)==True: 
                        #miramos si el numero tiene chances
                        sudoku[posicion_y][posicion_x].append(numero) #metemos el numero en esa probabilidad
        for posibilidades in range(0,len(sudoku)): # creo que es mejro que lo haga por fila porque por columa 
            #serian mas vueltas
            try: #evitar error al sacarle len() a un numero "5" en vez de a una lista
                if len(sudoku[posicion_y][posibilidades])==1: #si solo hay una posibilidad
                    sudoku[posicion_y][posibilidades]=sudoku[posicion_y][posibilidades][0]
                    #combertimos esa posibilidad en una realidad
            except: continue #que siga si encuentra un numero en vez de una lista
    for posicion_y in range(0,len(sudoku)): # para quitar las posibilidades y volver a empezar el tanteo
        for posicion_x in range(0,len(sudoku)):
            organizador_de_repeticion(sudoku,posicion_y,posicion_x)
    for posicion_y in range(0,len(sudoku)): # para quitar las posibilidades y volver a empezar el tanteo
        if repetir:
            break
        for posicion_x in range(0,len(sudoku)):
            if sudoku[posicion_y][posicion_x]==0:
                repetir=True
                break
            else:
                repetir=False
    if repetir:
        mostrar_pantalla(sudoku,contador)
        tecnica_tanteo(sudoku,contador+1)
    else:
        mostrar_pantalla(sudoku,contador)


tecnica_tanteo(sudoku2) #aqui pones el sudoku que quieres resolver