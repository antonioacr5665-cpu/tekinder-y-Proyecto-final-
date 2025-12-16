
import tkinter as tk
from tkinter import font

# ventana
ventana = tk.Tk()
ventana.title("Ventana de Bienvenida")
ventana.geometry("500x300")
ventana.configure(bg="#EDF2F7")  

# Configurar 
fuente_titulo = font.Font(family="Helvetica", size=24, weight="bold")
fuente_normal = font.Font(family="Arial", size=12)


label_bienvenida = tk.Label(
    ventana,
    text="¡Bienvenido a Tkinter!",
    font=fuente_titulo,
    fg="#2c3e50",      
    bg="#f0f8ff",      
    pady=30
)
label_bienvenida.pack()


label_descripcion = tk.Label(
    ventana,
    text="Esta es una ventana básica creada Por Antonio Carvajal con la biblioteca Tkinter",
    font=fuente_normal,
    fg="#34495e",
    bg="#f0f8ff"
)
label_descripcion.pack(pady=10)


label_info = tk.Label(
    ventana,
    text="Tkinter es la biblioteca estándar de Python\npara crear interfaces gráficas de usuario (GUI)",
    font=("Arial", 10, "italic"),
    fg="#7f8c8d",
    bg="#f0f8ff",
    justify="center"
)
label_info.pack(pady=20)

#salida
boton_salir = tk.Button(
    ventana,
    text="Cerrar Ventana",
    command=ventana.destroy,
    font=("Arial", 12),
    bg="#e74c3c",      
    fg="white",
    padx=30,
    pady=10,
    cursor="hand2",   
    relief="raised",   
    bd=3
)
boton_salir.pack(pady=20)


ventana.mainloop()