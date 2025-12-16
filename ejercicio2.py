import tkinter as tk
from tkinter import messagebox

def mostrar_texto():
    
    texto = entrada.get().strip()  
    
    if texto: 
        label_resultado.config(
            text=f"Texto ingresado: {texto}",
            fg="#27ae60",  # Verde
            font=("Arial", 12, "bold")
        )
       
        entrada.delete(0, tk.END)
        
        entrada.focus()
    else:
       
        messagebox.showwarning("Campo Vacío", "Por favor, escribe algo primero")
        label_resultado.config(
            text="Esperando texto...",
            fg="#e74c3c"  # Rojo
        )


ventana = tk.Tk()
ventana.title("Mostrar Texto")
ventana.geometry("600x300")
ventana.configure(bg="#f7f9f9")
ventana.resizable(False, False)  


frame_principal = tk.Frame(ventana, bg="#f7f9f9", padx=20, pady=20)
frame_principal.pack(expand=True, fill="both")


titulo = tk.Label(
    frame_principal,
    text="Ingresar y Mostrar Texto",
    font=("Arial", 18, "bold"),
    bg="#f7f9f9",
    fg="#2c3e50"
)
titulo.pack(pady=(0, 20))


instrucciones = tk.Label(
    frame_principal,
    text="Escribe cualquier texto en el campo de abajo y presiona el botón:",
    font=("Arial", 11),
    bg="#f7f9f9",
    fg="#34495e"
)
instrucciones.pack(pady=10)


entrada = tk.Entry(
    frame_principal,
    font=("Arial", 14),
    width=40,
    bd=3,
    relief="sunken",
    justify="center"
)
entrada.pack(pady=15)
entrada.focus()  


frame_botones = tk.Frame(frame_principal, bg="#f7f9f9")
frame_botones.pack(pady=10)


boton_mostrar = tk.Button(
    frame_botones,
    text="Mostrar Texto",
    command=mostrar_texto,
    font=("Arial", 12, "bold"),
    bg="#3498db",  # Azul
    fg="white",
    padx=25,
    pady=8,
    cursor="hand2",
    relief="raised",
    bd=2
)
boton_mostrar.pack(side="left", padx=10)


def limpiar_todo():
    entrada.delete(0, tk.END)
    label_resultado.config(
        text="Resultado aparecerá aquí...",
        fg="#7f8c8d",
        font=("Arial", 11)
    )

boton_limpiar = tk.Button(
    frame_botones,
    text="Limpiar Todo",
    command=limpiar_todo,
    font=("Arial", 12),
    bg="#95a5a6",  # Gris
    fg="white",
    padx=25,
    pady=8,
    cursor="hand2"
)
boton_limpiar.pack(side="left", padx=10)


label_resultado = tk.Label(
    frame_principal,
    text="Resultado aparecerá aquí...",
    font=("Arial", 11),
    bg="#ecf0f1",
    fg="#7f8c8d",
    width=50,
    height=3,
    relief="ridge",
    bd=2,
    wraplength=400  
)
label_resultado.pack(pady=20)


ventana.mainloop()