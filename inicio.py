from math import e
import math as math
import numpy as np
from sympy import Symbol
from sympy import lambdify
from scipy.optimize import fsolve

x = Symbol('x')
y = Symbol('y')

def f(a,b):
    return ((a*x) - (3*a)/(a + pow(e,(b*x))))

# Puntos fijos:

def puntosFijos(a, b):
    eq = f(a,b) - x
    res = lambdify(x, eq, modules=['numpy'])
    # xtol para terminar el calculo si el error entre dos iteraciones consecutivas es menor al dado
    value, info, ier, msg = fsolve(res, 0.5, xtol=1e-11, full_output=True)
    # Si no encuentra solucion ier == 0
    if ier != 1:
        return [0.]
    else:
        return value

if __name__ == '__main__':
    print("Escriba un intervalo para calcular los puntos extremos (desde 0 hasta el valor elegido): ", end="")
    intervalo = int(input())

    # Lista[float] para ir guardando los puntos fijos:
    puntosF = list()
    
    for a in range(intervalo):
        for b in range(intervalo):
            print()
            print("Para los valores de a y b: " + "[" + str(a) +", " + str(b) + "]")
            if (puntosFijos(a,b) != [0.] and int(puntosFijos(a,b)) == puntosFijos(a,b)):
                print("Tiene punto fijo en x = " + str(puntosFijos(a,b)[0]))
                puntosF.append(puntosFijos(a,b)[0])
            else:
                print("[" + str(a) + ", " + str(b) + "]" + " no tienen puntos fijos")
    
    print(puntosF)