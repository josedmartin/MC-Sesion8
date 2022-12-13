from tkinter import *
import tkinter.messagebox
import customtkinter
from math import e
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sympy import *
import main

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

x, y = symbols('x y')
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Interfaz para Graficar")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((5), weight=1)
        
        # Frame customizado para titulo y demas opciones
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=12, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        # Titulo para la app
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Graficador", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Botones dentro del frame
        # self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Calcular", command=self.sidebar_button_event)
        # self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        # create main entry and button
        #self.entry = customtkinter.CTkEntry(self, placeholder_text="Datos")
        # Para mostrar los resultados
        self.puntos = customtkinter.CTkLabel(self, text="Resultados: ", anchor="w")
        self.puntos.grid(row=9, column=1, padx=(20,10), pady=(10, 0))
        self.resultados = tkinter.Text(self,height=5, width=40, background="white")
        self.resultados.grid(row=10, column=1,rowspan=2, columnspan=6, padx=(20, 0), pady=(20, 50), sticky="nsew")

        self.entry1 = customtkinter.CTkEntry(self, placeholder_text="a ", width=50, height=10)
        self.entry1.grid(row=0, column=4, padx=(10, 20), pady=(50, 10), sticky="nsew")
        self.entry2 = customtkinter.CTkEntry(self, placeholder_text="b ", width=50, height=10)
        self.entry2.grid(row=1, column=4, padx=(10, 20), pady=(10, 10), sticky="nsew")
        self.entry3 = customtkinter.CTkEntry(self, placeholder_text="k ", width=100, height=10)
        self.entry3.grid(row=2, column=4, padx=(10, 20), pady=(10, 10), sticky="nsew")
        self.entry4 = customtkinter.CTkEntry(self, placeholder_text="x0 ", width=100, height=10)
        self.entry4.grid(row=3, column=4, padx=(10, 20), pady=(10, 10), sticky="nsew")
        self.entry5 = customtkinter.CTkEntry(self, placeholder_text="y0 ", width=100, height=10)
        self.entry5.grid(row=4, column=4, padx=(10, 20), pady=(10, 10), sticky="nsew")

        # crea grafica
        self.grafica = customtkinter.CTkCanvas(self,height=25, width=25, background="grey")
        self.grafica.grid(row=0, column=1,rowspan=6, columnspan=3, padx=(100, 100), pady=(50, 50), sticky="nsew")
        
        # crea radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=7,rowspan=6, padx=(20, 50), pady=(50, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Tipo de gráfica:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0, text="Función")
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1, text="Órbita")
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2, text="Atractores")
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        

        # create main entry and button
        self.main_button_1 = customtkinter.CTkButton(master=self, text="Calcular", fg_color="SpringGreen4", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.Calcular)
        self.main_button_1.grid(row=10, column=7, padx=(20, 50), pady=(20, 10), sticky="nsew")
        self.main_button_2 = customtkinter.CTkButton(master=self, text="Borrar", fg_color="firebrick4", border_width=2, text_color=("gray10", "#DCE4EE"),  command=self.Borrar)
        self.main_button_2.grid(row=11, column=7, padx=(20, 50), pady=(10, 50), sticky="nsew")

        

        # Para configurar la pantalla
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Apariencia:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Escalado de Interfaz:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
    
    #Borrar todo lo introducido y obtenido
    def Borrar(self):
        self.resultados.delete(1.0, END)
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry5.delete(0, END)
        # Para borrar la grafica
        try: 
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError: 
            pass

    # Crea una función para dibujar la gráfica de la función y mostrar calculos en pantalla
    def Calcular(self):
        if self.entry1.get() == '':
            a = 0.0
        else:
            a = float(self.entry1.get())
        if self.entry2.get() == '':
            b = 0.0
        else:
            b = float(self.entry2.get())
        if self.entry3.get() == '':
            k = 0.0
        else:
            k = float(self.entry3.get())

        fk = main.recursividad_fx(a,b,k)
        gk = main.recursividad_gy(a,b,k)
        value0 = self.radio_button_1._variable.get()
        value1 = self.radio_button_2._variable.get()
        value2 = self.radio_button_3._variable.get()
        if value0 == 0:
            # Calculo funcion
            #Calculo de los puntos fijos
            puntos_fijos = main.puntosFijos_fx(a,b,k)
            #puntos_fijos = nonlinsolve([Eq(fk, x), Eq(gk, y)], (x, y))
            self.resultados.insert(1.0, "Puntos fijos: " + str(puntos_fijos))
            #Calculamos la estabilidad de los puntos fijos mediante la funcion estabilidad
            #res = main.estabilidad(fx, gy, puntos_fijos)
            #self.resultados.insert('2.0', "\nEstabilidad: " + str(res))
            # Define la función a graficar
            def f(x):
                return ((a*x) - (3*b)/(a + pow(e,(b*x))))

            # Crea una figura y un eje para la gráfica
            fig, ax = plt.subplots()

            # Calcula los valores de x y y para la gráfica
            x1 = np.linspace(-10, 10, 100)
            f1 = f(x1)

            # Dibuja la gráfica de la función
            ax.plot(x1, f1)
    
            # Crea una instancia de FigureCanvasTkAgg utilizando la instancia de Figure
            self.canvas = FigureCanvasTkAgg(fig, master=self.grafica)
            # Obtiene el widget que se mostrará en la interfaz de usuario
            widget = self.canvas.get_tk_widget()
            # Muestra el widget
            widget.pack()

        elif value1 == 1:
            # Calculo orbita
            self.resultados.delete(1.0, tkinter.END)
            #Calculamos la matriz jacobiana
            # j = [[simplify(i) for i in x] for x in Matrix([fx, gy]).jacobian(Matrix([x, y])).tolist()]
            # self.resultados.insert('3.0', "\nJacobiana: " + str(j))
            # #Para los puntos fijos obtenidos calculamos los autovalores
            # f_eigen_values = list(Matrix([fx, gy]).jacobian(Matrix([x, y])).eigenvals().keys())

            # eigen_values = [list(simplify(f.subs({x:p[0], y:p[1]})) for f in f_eigen_values) for p in puntos_fijos]

            # self.resultados.insert('4.0', "\nAutovalores: " + str(eigen_values))
            
            # #Valores para calcular los exponentes de Lyapunov
            # x0 = float(self.entry4.get())
            # y0 = float(self.entry5.get())

            # #Calculamos los exponentes de Lyapunov
            # n_lyapunov = main.lyapunov_n(fx, gy, x0, y0)
            # self.resultados.insert('5.0', "\nNumero de Lyapunov: " + str(n_lyapunov))
            # exp_lyapunov = list(map(lambda x: ln(x), n_lyapunov))
            # self.resultados.insert('6.0', "\nExponentes de Lyapunov: " + str(exp_lyapunov))

            # #Ver si hay órbitas caóticas para x0 e y0
            # if (exp_lyapunov[0] > 0 and exp_lyapunov[1] != 0) : # tengamos un exponente mayor que 0 y otro distinto de 0
            #     #Para que sea asintoticamente periodica, tiene que serlo tambien para la orbita periodica, entoces
            #     #ambas orbitas tendrán el mismo exponente de Lyapunov.
            #     if (exp_lyapunov[0] == exp_lyapunov[1]) : 
            #         self.resultados.insert('7.0', "\nHay orbitas caoticas")
            # else :
            #     self.resultados.insert('8.0', "\nNo se encuentran Orbitas Caoticas")
            funcion = "Orbitas"
            self.resultados.insert(1.0, funcion)
        elif value2 == 2:
            # Calculo atractores
            self.resultados.delete(1.0, tkinter.END)
            funcion = "Atractores"
            self.resultados.insert(1.0, funcion)

        

        

        
        
        

        

        # Define la función a graficar
        #def f(x):
        #    return ((a*x) - (3*b)/(a + pow(e,(b*x))))

        # Crea una figura y un eje para la gráfica
        #fig, ax = plt.subplots()

        # Calcula los valores de x y y para la gráfica
        #x1 = np.linspace(-10, 10, 100)
        #f1 = f(x1)

        # Dibuja la gráfica de la función
        #ax.plot(x1, f1)
  
        # Crea una instancia de FigureCanvasTkAgg utilizando la instancia de Figure
        #canvas = FigureCanvasTkAgg(fig, master=self.textbox)
        # Obtiene el widget que se mostrará en la interfaz de usuario
        #widget = canvas.get_tk_widget()
        # Muestra el widget
        #widget.pack()

    
        

if __name__ == "__main__":
    app = App()
    app.mainloop()