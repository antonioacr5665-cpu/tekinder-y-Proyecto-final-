import tkinter as tk


dibujando = False
ultimo_x = 0
ultimo_y = 0
color_actual = "black"
grosor = 3

def empezar_dibujo(evento):
    global dibujando, ultimo_x, ultimo_y
    dibujando = True
    ultimo_x = evento.x
    ultimo_y = evento.y
    
    
    lienzo.create_oval(evento.x-2, evento.y-2, 
                      evento.x+2, evento.y+2, 
                      fill=color_actual, 
                      outline=color_actual)

def dibujar_linea(evento):
    global dibujando, ultimo_x, ultimo_y
    
    if dibujando:
       
        lienzo.create_line(ultimo_x, ultimo_y, 
                          evento.x, evento.y, 
                          fill=color_actual, 
                          width=grosor)
        
        
        ultimo_x = evento.x
        ultimo_y = evento.y

def terminar_dibujo(evento):
    global dibujando
    dibujando = False

def cambiar_color(nuevo_color):
    global color_actual
    color_actual = nuevo_color
    etiqueta_color.config(text=f"Color: {nuevo_color}", 
                         fg=nuevo_color if nuevo_color != "black" else "white",
                         bg=nuevo_color)

def cambiar_grosor(nuevo_grosor):
    global grosor
    grosor = nuevo_grosor
    etiqueta_grosor.config(text=f"Grosor: {grosor}")

def limpiar_lienzo():
    lienzo.delete("all")
    etiqueta_info.config(text="Lienzo limpiado")


ventana = tk.Tk()
ventana.title(" Programa para Dibujar Desarrollado Por Antonio Carvajal")
ventana.geometry("700x600")
ventana.configure(bg="gray")


titulo = tk.Label(ventana,
                 text="MI PROGRAMA PARA DIBUJAR",
                 font=("Arial", 16, "bold"),
                 bg="gray",
                 fg="white")
titulo.pack(pady=10)


panel_controles = tk.Frame(ventana, bg="darkgray", height=50)
panel_controles.pack(fill="x", padx=10, pady=5)


instrucciones = tk.Label(panel_controles,
                        text="¡Mantén click y arrastra para dibujar!",
                        font=("Arial", 10),
                        bg="darkgray",
                        fg="yellow")
instrucciones.pack(side="left", padx=10)


tk.Label(panel_controles, text="", bg="darkgray", width=5).pack(side="left")


colores = [
    ("Negro", "black"),
    ("Rojo", "red"),
    ("Azul", "blue"),
    ("Verde", "green"),
    ("Amarillo", "yellow"),
    ("Borrador", "white")
]

for nombre, color in colores:
    if color == "white":
        btn = tk.Button(panel_controles,
                       text=nombre,
                       command=lambda c=color: cambiar_color(c),
                       bg=color,
                       fg="black",
                       font=("Arial", 9),
                       width=8)
    else:
        btn = tk.Button(panel_controles,
                       text=nombre,
                       command=lambda c=color: cambiar_color(c),
                       bg=color,
                       fg="white",
                       font=("Arial", 9),
                       width=8)
    btn.pack(side="left", padx=2)


tk.Label(panel_controles, 
        text="  Grosor:", 
        bg="darkgray",
        fg="white").pack(side="left", padx=10)

grosor_var = tk.IntVar(value=grosor)
spinbox_grosor = tk.Spinbox(panel_controles,
                           from_=1,
                           to=10,
                           textvariable=grosor_var,
                           width=5,
                           command=lambda: cambiar_grosor(grosor_var.get()))
spinbox_grosor.pack(side="left", padx=5)


btn_limpiar = tk.Button(panel_controles,
                       text="Limpiar Todo",
                       command=limpiar_lienzo,
                       bg="orange",
                       fg="black",
                       font=("Arial", 9, "bold"))
btn_limpiar.pack(side="right", padx=10)


marco_lienzo = tk.Frame(ventana, bg="white", bd=3, relief="sunken")
marco_lienzo.pack(padx=20, pady=10, fill="both", expand=True)


lienzo = tk.Canvas(marco_lienzo, bg="white", cursor="cross")
lienzo.pack(fill="both", expand=True, padx=2, pady=2)


lienzo.bind("<Button-1>", empezar_dibujo)
lienzo.bind("<B1-Motion>", dibujar_linea)
lienzo.bind("<ButtonRelease-1>", terminar_dibujo)


panel_info = tk.Frame(ventana, bg="gray", height=40)
panel_info.pack(fill="x", padx=10, pady=5)


etiqueta_color = tk.Label(panel_info,
                         text="Color: black",
                         font=("Arial", 10, "bold"),
                         bg="black",
                         fg="white",
                         width=15)
etiqueta_color.pack(side="left", padx=10)


etiqueta_grosor = tk.Label(panel_info,
                          text=f"Grosor: {grosor}",
                          font=("Arial", 10),
                          bg="gray",
                          fg="white")
etiqueta_grosor.pack(side="left", padx=20)


etiqueta_info = tk.Label(panel_info,
                        text="Presiona en el área blanca y arrastra para dibujar",
                        font=("Arial", 9, "italic"),
                        bg="gray",
                        fg="lightgreen")
etiqueta_info.pack(side="right", padx=10)




ventana.mainloop()