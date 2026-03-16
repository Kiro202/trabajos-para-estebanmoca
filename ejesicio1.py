#Ejercicio: "El Historial de Navegación Recursivo"
#Problema: Estás diseñando un navegador web sencillo. 
# Cada vez que el usuario visita una página, esta se guarda. 
# El usuario quiere una función que le permita "retroceder" N pasos en su historial, 
# pero con una condición: si en el camino encuentra una página de "Error 404",
#  el proceso de retroceso debe detenerse inmediatamente por seguridad.

#El Reto: Escribir una función recursiva retroceder(historial, pasos) 
# que elimine las páginas visitadas una a una hasta cumplir con el número 
# de pasos o encontrar el error.
historial=["pollo","Error 404","lucas","sorteo","furroslandia"]
def retroceder_historial(historial,paso):
    if paso==0:
        return f"Hemos llegado hasta {historial[len(historial)-1]}"
    elif historial[len(historial)-1]==False:
        return "No queda más"
    elif historial[len(historial)-1]=="Error 404":
        return "error en la pagina"
    else:
        print(f"estamos en {historial[len(historial)-1]}")
        historial.pop()
        print(historial)
        return retroceder_historial(historial,paso-1)

def Navegador():
    menu=int(input('            BIENVENIDO（〃｀ 3′〃）\n¿Que desceas hacer?\n1.hacer tu busqueda\n2.retroceder historial o((⊙﹏⊙))o.\n3.salir\n dijita tu eleccion: '))
    if menu==1:
        pagina=input("'Haz tu busqueda'\nGoogle:")
        historial.append(pagina)
        print(historial)
        Navegador()
    if menu==2:
        pasos=int(input("cuantos pasos atas quiere dar?"))
        resultado=retroceder_historial(historial,pasos+1)
        print(resultado)
        Navegador()
    if menu==3:
        print("adios")
        return
Navegador()
    
    