from sympy import symbols, Or, And, Implies,Equivalent
from sympy.logic.boolalg import truth_table
    
# Determina si todos los productos tienen stock mayor a 0 (∀)
# Determina si al menos uno de los productos es de tipo "Lujo" (∃)

productos = [
    {"nombre": "Pan", "stock": 10, "tipo": "Basico"},
    {"nombre": "Reloj", "stock": 0, "tipo": "Lujo"}
]

# Cuantificador universal
todos_stocks = all(p["stock"] > 0 for p in productos)

# Cuantificador existencial
uno_lujo = any(p["tipo"] == "Lujo" for p in productos)

print("¿Todos los productos tienen stock > 0?:", todos_stocks)
print("¿Existe al menos un producto de lujo?:", uno_lujo)