import math
import numpy as np
from sympy import *
from scipy.optimize import fsolve

x = Symbol('x')
y = Symbol('y')

def f_inicial(a,b):
    return a*x - (3*a)/(a + math.e**(b*x))

def puntosFijos(a, b):
    eq = f_inicial(a,b) - x
    func = lambdify(x, eq, 'numpy')
    res = func(x)
    
    if res != []:
        return "Puntos fijos: " + str(res)
    else:
        return "No hay puntos fijos"

def estabilidad(f,p):
    v = f(x).diff(x)
    res = solve(v,x)
    mensaje = ""
    if res > 1 :
        mensaje = "El punto " + p + " es repulsivo."
    else :
        if res < 1:
            mensaje = "El punto " + p + " es actractivo."
        else:
            mensaje = "El punto " + p + " es indiferente."
    return mensaje

if __name__ == "__main__":
    print("Escribe parametro a: ")
    a = float(input())
    print("Escribe parametro b: ")
    b = float(input())
    print(f_inicial(a,b))
    print(puntosFijos(a,b))
