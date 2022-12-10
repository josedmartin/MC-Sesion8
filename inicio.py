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
    eq = f(a,b) - x
    res = lambdify(x, eq, modules=['numpy'])
    # xtol para terminar el calculo si el error entre dos iteraciones consecutivas es menor al dado
    value, info, ier, msg = fsolve(res, 0.5, xtol=1e-11, full_output=True)
    # Si no encuentra solucion ier == 0
    if ier != 1:
        return [0.]
    else:
        return value

def estabilidad(f,ptos_fijos):
    for pf in ptos_fijos:
        v = sp.diff(f, x).subs(x,pf) #Derivamos y sustituimos por el valor
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
        return mensaje

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

    print("A")
    a = int(input())
    print("B")
    b = int(input())

    print("Funcion inicial: " + str(f(a,b)) + "\n")

    pts = puntosFijos(a, b)

    print("Puntos fijos: " + str(pts) + "\n")

    res = estabilidad(f(a,b),pts[0])

    print(res)

