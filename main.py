from sympy import *
from math import e
import numpy as np
import matplotlib.pyplot as plt

x, y = symbols('x y')

def f(a,b,x):
    return ((a*x) - (3*a)/(a + pow(e,(b*x))))

def fg(a,b):
    return ( a*y + ((a*x) - (3*a)/(a + pow(e,(b*x)))), a*y + ((a*x) - (3*a)/(a + pow(e,(b*x)))) )

#Calculo de cualquier punto periodico de periodo k 
def recursividad_fx(a,b,k):
    if k == 1:  # Condición de parada
        return a*y + ((a*x) - (3*a)/(a + pow(e,(b*x)))) 
    else:  # Caso recursivo
        return a*y + ((a*recursividad_fx(a,b,k-1)) - (3*a)/(a + pow(e,(b*recursividad_fx(a,b,k-1)))))

def recursividad_gy(a,b,k):
    if k == 1:  # Condición de parada
        return (a*x + a*y - 3*a/(a + pow(e,(b*x))))*x - x - 3*(a*x + a*y - 3*a/(a + pow(e,(b*x))))/(a*x + a*y - 3*a/(a + pow(e,(b*x))) + pow(e,(b*x)))
    else:  # Caso recursivo
        return (a*x + a*recursividad_gy(a,b,k-1) - 3*a/(a + pow(e,(b*x))))*x - x - 3*(a*x + a*recursividad_gy(a,b,k-1) - 3*a/(a + pow(e,(b*x))))/(a*x + a*recursividad_gy(a,b,k-1) - 3*a/(a + pow(e,(b*x))) + pow(e,(b*x)))

def puntosFijos_fx(a, b, k):
    funcion = recursividad_fx(a,b,k)
    puntosF = list()
    try:
        puntos = solve([funcion-x], [x], dict=True)
        for p in puntos:
            if (p != 'zoo' or p != '-zoo'):
                puntosF.append(p)
    except Exception:
        pass
    return puntosF

def puntosFijos_gy(a, b, k):
    funcion = recursividad_gy(a,b,k)
    puntosF = list()
    try:
        puntos = solve([funcion-y], [y], dict=True)
        for p in puntos:
            if (p != 'zoo' or p != '-zoo'):
                puntosF.append(p)
    except Exception:
        pass
    return puntosF

def estabilidad(f, g, fixed_points):
    estabilidad = list()
    Df = Matrix([f, g]).jacobian(Matrix([x, y]))

    for point in fixed_points:
        eigen_values = list(
            Df.subs({x: point[0], y: point[1]}).eigenvals().keys())

        if im(eigen_values[0]) != 0:
            a = re(eigen_values[0])
            b = im(eigen_values[0])
            r = sqrt((a**2) + (b**2))
            if abs(r) < 1:
                estabilidad.append((point, "punto atractivo."))
            else:
                estabilidad.append((point, "punto repulsivo."))
        
        elif len(set(eigen_values)) == 2 and im(eigen_values[1]) != 0:
            a = re(eigen_values[1])
            b = im(eigen_values[1])
            r = sqrt((a**2) + (b**2))
            if abs(r) < 1:
                estabilidad.append((point, "punto atractivo."))
            else:
                estabilidad.append((point, "punto repulsivo.")) 

        else:
            if len(set(eigen_values)) == 2:
                if (abs(eigen_values[0]) < 1 and 1 < abs(eigen_values[1])) or (abs(eigen_values[1]) < 1 and 1 < abs(eigen_values[0])):
                    estabilidad.append((point, "punto de silla."))
                if 0 < abs(eigen_values[0]) < 1 and 0 < abs(eigen_values[1]) < 1:
                    estabilidad.append((point, "punto atractivo."))
                if 1 < abs(eigen_values[0]) and 1 < abs(eigen_values[1]):
                    estabilidad.append((point, "punto repulsivo."))

            if len(set(eigen_values)) == 1:
                if abs(eigen_values[0]) < 1:
                    estabilidad.append((point, "punto atractivo."))
                else:
                    estabilidad.append((point, "punto repulsivo."))

    return estabilidad

def lyapunov_n(f, g, x0, y0):
    vec = Matrix([f, g])
    fx = vec.diff(x)
    fy = vec.diff(y)
    A = Matrix([[fx, fy]])
    A_t = A.transpose()
    return list(map(lambda x: sqrt(x), list((A*A_t).subs({x: x0, y: y0}).eigenvals().keys())))

if __name__ == '__main__':

    print("Introduce el valor de A: ")
    a = int(input())
    print("Introduce el valor de B: ")
    b = int(input())

    fx = a*y + f(a,b,x) 
    gy = -x + f(a,b,fx)

    print("Introduce el valor de k: ")
    k = int(input())

    fk = recursividad_fx(a,b,k)
    gk = recursividad_gy(a,b,k)

    #Calculo de los puntos fijos
    puntos_fijos = nonlinsolve([Eq(fk, x), Eq(gk, y)], (x, y))
    print(f"puntos fijos:{puntos_fijos}")

    #Calculamos la estabilidad de los puntos fijos mediante la funcion estabilidad
    res = estabilidad(fx, gy, puntos_fijos)
    print(f"estabilidad: {res}")

    #Calculamos la matriz jacobiana
    j = [[simplify(i) for i in x] for x in Matrix([fx, gy]).jacobian(Matrix([x, y])).tolist()]
    print(f"Jacobiana:{j}")

    #Para los puntos fijos obtenidos calculamos los autovalores
    f_eigen_values = list(Matrix([fx, gy]).jacobian(Matrix([x, y])).eigenvals().keys())

    eigen_values = [list(simplify(f.subs({x:p[0], y:p[1]})) for f in f_eigen_values) for p in puntos_fijos]

    print(f"Autovalores: {eigen_values}")
    
    #Valores para calcular los exponentes de Lyapunov
    print("Introduce el valor de x0: ")
    x0 = int(input())
    print("Introduce el valor de y0: ")
    y0 = int(input())

    #Calculamos los exponentes de Lyapunov
    n_lyapunov = lyapunov_n(fx, gy, x0, y0)
    print(f"Numero de Lyapunov {n_lyapunov}")
    exp_lyapunov = list(map(lambda x: ln(x), n_lyapunov))
    print(f"Exponentes de Lyapunov {exp_lyapunov}")

    #Ver si hay órbitas caóticas para x0 e y0
    if (exp_lyapunov[0] > 0 and exp_lyapunov[1] != 0) : # tengamos un exponente mayor que 0 y otro distinto de 0
        #Para que sea asintoticamente periodica, tiene que serlo tambien para la orbita periodica, entoces
        #ambas orbitas tendrán el mismo exponente de Lyapunov.
        if (exp_lyapunov[0] == exp_lyapunov[1]) : 
            print("Hay orbitas caoticas")
    else :
        print("No se encuentran Orbitas Caoticas")

        
