from sympy import symbols, Or, And, Implies,Equivalent
from sympy.logic.boolalg import truth_table
def boleado(variable):
    if variable=="s":variable=True
    else:variable=False
    return variable
while True:
    C=boleado(input("la clave es correcta?s/n "))
    R=boleado(input("la escaner de retina es correcta?s/n "))
    E=boleado(input("la llave de seguridad es correcta?s/n "))
    B=True

    argumento=Equivalent(B,Or(And(C,R),E))
    #input(argumento) #true
    input("bodega abierta?:"+str(argumento))
    
#La bóveda se abre ($B$) si y solo si se introduce la clave correcta ($C$) y 
# el escáner de retina es positivo ($R$), o si se activa la llave de emergencia ($E$).