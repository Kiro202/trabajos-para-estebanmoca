from sympy import symbols, Or, And, Implies,Equivalent
from sympy.logic.boolalg import truth_table

def boleado(variable):
    if variable=="s":variable=True
    else:variable=False
    return variable

facts ={"estrato": True,
     "promedio": True}


facts['estrato']=boleado(input("tiene estrato menor a 3?s/n"))
if facts['estrato']:
    facts['promedio']=boleado(input("tiene promedio mayor a 8?s/n"))
else:
    facts['promedio']=boleado(input("tiene promedio mayor o igual a 9?s/n"))

# Cuantificador existencial
uno_lujo = Or(facts["promedio"],And(facts["promedio"],facts["estrato"]))

print("es becado el estuidante?:"+ str(uno_lujo))



