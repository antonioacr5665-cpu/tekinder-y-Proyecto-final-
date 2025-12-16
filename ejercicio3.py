import tkinter as tk
from tkinter import messagebox

def calcular():
    
    try:
       
        num1 = float(entrada_num1.get())
        num2 = float(entrada_num2.get())
        
     
        resultado = num1 + num2
        
        label_resultado.config(
            text=f"{num1} + {num2} = {resultado}",
            fg="#27ae60",  # Verde
            font=("Arial", 14, "bold")
        )
        
    except ValueError:
       
        messagebox.showerror("Error", "Por favor, ingresa números válidos")
        label_resultado.config(
            text="Error: Ingresa solo números",
            fg="#e74c3c"  # Rojo
        )

def limpiar():
    """Limpia todos los campos"""
    entrada_num1.delete(0, tk.END)
    entrada_num2.delete(0, tk.END)
    label_resultado.config(
        text="Resultado aparecerá aquí",
        fg="#7f8c8d",
        font=("Arial", 11)
    )
    entrada_num1.focus()


ventana = tk.Tk()
ventana.title("Calculadora de Suma")
ventana.geometry("500x400")
ventana.configure(bg="#f0f3f4")


titulo = tk.Label(
    ventana,
    text="CALCULADORA DE SUMA",
    font=("Arial", 20, "bold"),
    bg="#f0f3f4",
    fg="#2c3e50"
)
titulo.pack(pady=20)

# Frame para entradas
frame_entradas = tk.Frame(ventana, bg="#f0f3f4")
frame_entradas.pack(pady=20)

# Primer número
label_num1 = tk.Label(
    frame_entradas,
    text="Primer número:",
    font=("Arial", 12),
    bg="#f0f3f4",
    width=15,
    anchor="e"
)
label_num1.grid(row=0, column=0, padx=10, pady=10)

entrada_num1 = tk.Entry(
    frame_entradas,
    font=("Arial", 14),
    width=15,
    bd=2,
    relief="groove",
    justify="center"
)
entrada_num1.grid(row=0, column=1, padx=10, pady=10)

# Segundo número
label_num2 = tk.Label(
    frame_entradas,
    text="Segundo número:",
    font=("Arial", 12),
    bg="#f0f3f4",
    width=15,
    anchor="e"
)
label_num2.grid(row=1, column=0, padx=10, pady=10)

entrada_num2 = tk.Entry(
    frame_entradas,
    font=("Arial", 14),
    width=15,
    bd=2,
    relief="groove",
    justify="center"
)
entrada_num2.grid(row=1, column=1, padx=10, pady=10)


frame_botones = tk.Frame(ventana, bg="#f0f3f4")
frame_botones.pack(pady=20)

# Botón calcular
boton_calcular = tk.Button(
    frame_botones,
    text="Calcular Suma",
    command=calcular,
    font=("Arial", 12, "bold"),
    bg="#2ecc71",  # Verde
    fg="white",
    padx=20,
    pady=10,
    cursor="hand2"
)
boton_calcular.pack(side="left", padx=10)


boton_limpiar = tk.Button(
    frame_botones,
    text="Limpiar Campos",
    command=limpiar,
    font=("Arial", 12),
    bg="#e74c3c",  # Rojo
    fg="white",
    padx=20,
    pady=10,
    cursor="hand2"
)
boton_limpiar.pack(side="left", padx=10)


frame_resultado = tk.Frame(ventana, bg="#d5dbdb", bd=3, relief="sunken")
frame_resultado.pack(pady=20, padx=20, fill="x")

label_titulo_resultado = tk.Label(
    frame_resultado,
    text="RESULTADO:",
    font=("Arial", 12, "bold"),
    bg="#d5dbdb",
    fg="#2c3e50"
)
label_titulo_resultado.pack(pady=(10, 5))

label_resultado = tk.Label(
    frame_resultado,
    text="Resultado aparecerá aquí",
    font=("Arial", 11),
    bg="#d5dbdb",
    fg="#7f8c8d",
    height=3
)
label_resultado.pack(pady=(5, 10))


label_info = tk.Label(
    ventana,
    text="Ingresa dos números y presiona 'Calcular Suma'",
    font=("Arial", 9, "italic"),
    bg="#f0f3f4",
    fg="#7f8c8d"
)
label_info.pack(pady=10)


entrada_num1.focus()


ventana.mainloop()