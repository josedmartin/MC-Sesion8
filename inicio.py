from math import e
from sympy import Symbol
from sympy import lambdify
from scipy.optimize import fsolve
import sympy as sp

x = Symbol('x')
y = Symbol('y')

def f(a,b):
    return ((a*x) - (3*a)/(a + pow(e,(b*x))))

# Puntos fijos:
def puntosFijos(a, b):
    puntosF = list()
    try:
        puntos = sp.solve([f(a,b)-x], [x], dict=True)
        for p in puntos:
            if (p != 'zoo' or p != '-zoo'):
                puntosF.append(p)
    except Exception:
        pass
    return puntosF

def estabilidad(f,ptos_fijos):
    aux = set()
    for pf in ptos_fijos:
        p = pf[x]
        aux.add(p)

    for punto in aux:
        print("ESTAMOS MIRANDO EL PUNTO: " + str(punto))
        v = sp.diff(f, x).subs(x,punto) #Derivamos y sustituimos por el valor
        res  = abs(v)
        print("VALOR OBTENIDO DERIVADA: " + str(res))
        mensaje = ""
        if res > 1 :
            mensaje = "El punto " + str(pf) + " es repulsivo."
        else :
            if res < 1:
                mensaje = "El punto " + str(pf) + " es actractivo."

                if res == 0:
                    mensaje = "El punto " + str(pf) + " es super actractivo."
                else:
                    mensaje = "El punto " + str(pf) + " es indiferente."
        print (mensaje)

if __name__ == '__main__':
    # print("Escriba un intervalo para calcular los puntos extremos (desde 0 hasta el valor elegido): ", end="")
    # intervalo = int(input())

    # # Lista[float] para ir guardando los puntos fijos:
    # puntosF = list()
    
    # for a in range(intervalo):
    #     for b in range(intervalo):
    #         print()
    #         print("Para los valores de a y b: " + "[" + str(a) +", " + str(b) + "]")
    #         if (puntosFijos(a,b) != [0.] and int(puntosFijos(a,b)) == puntosFijos(a,b)):
    #             print("Tiene punto fijo en x = " + str(puntosFijos(a,b)[0]))
    #             puntosF.append(puntosFijos(a,b)[0])
    #         else:
    #             print("[" + str(a) + ", " + str(b) + "]" + " no tienen puntos fijos")
    
    # print(puntosF)

    print("Introduce el valor de A: ")
    a = int(input())
    print("Introduce el valor de B: ")
    b = int(input())

    print("Funcion inicial: " + str(f(a,b)) + "\n")

    puntosF = puntosFijos(a, b)

    print("Puntos fijos: " + str(puntosF) + "\n")

    estabilidad(f(a,b),puntosF)


