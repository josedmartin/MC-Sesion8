import tkinter
import tkinter.messagebox
import customtkinter
from math import e
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sympy import Symbol

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Interfaz para Graficar")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
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
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Datos")
        self.entry.grid(row=11, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.entry1 = customtkinter.CTkEntry(self, placeholder_text="Valor para alpha: ", width=100, height=10)
        self.entry1.grid(row=5, column=1, padx=(20, 0), pady=(20, 10), sticky="nsew")
        self.entry2 = customtkinter.CTkEntry(self, placeholder_text="Valor para beta: ", width=100, height=10)
        self.entry2.grid(row=5, column=2, padx=(20, 0), pady=(20, 10), sticky="nsew")
        self.entry3 = customtkinter.CTkEntry(self, placeholder_text="Valor para k: ", width=100, height=10)
        self.entry3.grid(row=7, column=1, padx=(20, 0), pady=(20, 10), sticky="nsew")
        self.entry4 = customtkinter.CTkEntry(self, placeholder_text="Valor para x0: ", width=100, height=10)
        self.entry4.grid(row=7, column=2, padx=(20, 0), pady=(20, 10), sticky="nsew")
        self.entry5 = customtkinter.CTkEntry(self, placeholder_text="Valor para y0: ", width=100, height=10)
        self.entry5.grid(row=9, column=1, padx=(20, 0), pady=(20, 10), sticky="nsew")
        
        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=5, column=3, rowspan=5, padx=(20, 20), pady=(20, 0), sticky="nsew")
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
        self.main_button_1 = customtkinter.CTkButton(master=self, text="Calcular", fg_color="RoyalBlue2", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.plot_function)
        self.main_button_1.grid(row=10, column=3, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.main_button_2 = customtkinter.CTkButton(master=self, text="Borrar", fg_color="firebrick3", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                     command=self.borrar)
        self.main_button_2.grid(row=11, column=3, padx=(20, 20), pady=(10, 10), sticky="nsew")

        # create textbox
        self.textbox = tkinter.Text(self, width=250, background="gray30")
        self.textbox.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")





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
    
    
    x = Symbol('x')
    # Crea una función para dibujar la gráfica de la función
    def plot_function(self):
        a = float(self.entry1.get())
        b = float(self.entry2.get())
        # Define la función a graficar
        def f(x):
            return ((a*x) - (3*b)/(a + pow(e,(b*x))))

        # Crea una figura y un eje para la gráfica
        fig, ax = plt.subplots()

        # Calcula los valores de x y y para la gráfica
        x1 = np.linspace(-10, 10, 100)
        y = f(x1)

        # Dibuja la gráfica de la función
        ax.plot(x1, y)
        
        # Crea una instancia de FigureCanvasTkAgg utilizando la instancia de Figure
        canvas = FigureCanvasTkAgg(fig, master=self.textbox)
        # Obtiene el widget que se mostrará en la interfaz de usuario
        widget = canvas.get_tk_widget()
        # Muestra el widget
        widget.pack()
        

if __name__ == "__main__":
    app = App()
    app.mainloop()