from sympy import symbols, Or, And, Implies,Equivalent
from sympy.logic.boolalg import truth_table

def boleado(variable):
    if variable=="s":variable=True
    else:variable=False
    return variable
# Motor de inferencia: encadenamiento hacia adelante

# Reglas (premisas -> conclusión)
rules = [
    (['fiebre', 'tos'], 'gripe'),
    (['gripe'], 'descanso')
]

# Hechos iniciales
facts = {
    'fiebre': True,
    'tos': True
}

facts['fiebre']=boleado(input("tiene fiebre?s/n"))
facts['tos']=boleado(input("tiene tos?s/n"))

# Encadenamiento hacia adelante
for condiciones, conclusion in rules:
    if all(facts.get(c, False) for c in condiciones):
        facts[conclusion] = True
    else:facts[conclusion] = False

print("necesita descanso?"+str(facts[conclusion]))