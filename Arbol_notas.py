# =============================================
# ÁRBOL BINARIO DE BÚSQUEDA (BST)
# =============================================

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class BST:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)
        if valor < nodo.valor:
            nodo.izquierda = self._insertar(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._insertar(nodo.derecha, valor)
        return nodo

    def buscar(self, valor):
        return self._buscar(self.raiz, valor)

    def _buscar(self, nodo, valor):
        if nodo is None or nodo.valor == valor:
            return nodo
        if valor < nodo.valor:
            return self._buscar(nodo.izquierda, valor)
        return self._buscar(nodo.derecha, valor)

    # InOrder: recorre izq → raíz → der (resultado ordenado)
    def inorder(self, nodo="__raiz__"):
        if nodo == "__raiz__":
            nodo = self.raiz
        if nodo:
            yield from self.inorder(nodo.izquierda)
            yield nodo.valor
            yield from self.inorder(nodo.derecha)
    def minimo(self):
        valores=list(self.inorder())
        return valores[0]
    def maximo(self):
        valores=list(self.inorder())
        return valores[len(valores)-1]
    def top_n(self, n):
        valores=list(self.inorder())
        top=[]
        for i in range(0,n):
            top.append(valores[len(valores)-1-i])
        return top



# Prueba:
torneo = BST()
puntos = [3200, 4100, 1800, 5000, 2700, 3900, 4600]
for p in puntos:
    torneo.insertar(p)
    

print("Mínimo:", torneo.minimo())    # → 1800
print("Máximo:", torneo.maximo())    # → 5000
print("Top 3:",  torneo.top_n(1))    # → [5000, 4600, 4100]