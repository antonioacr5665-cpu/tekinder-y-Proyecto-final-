import tkinter as tk

def agregar_item():
    
    texto = entrada_texto.get()
    
    
    if texto != "":
        lista_elementos.insert(tk.END, texto)
        entrada_texto.delete(0, tk.END)  
        
        
        total = lista_elementos.size()
        etiqueta_contador.config(text=f"Hay {total} elementos")
    else:
        
        etiqueta_contador.config(text="¡Escribe algo primero!")

def borrar_item():
    try:
       
        seleccionado = lista_elementos.curselection()[0]
        lista_elementos.delete(seleccionado)
        
        
        total = lista_elementos.size()
        etiqueta_contador.config(text=f"Hay {total} elementos")
    except:
       
        etiqueta_contador.config(text="Selecciona algo para borrar")


ventana = tk.Tk()
ventana.title("Mi Lista de Cosas")
ventana.geometry("400x500")
ventana.configure(bg="lightblue")


titulo = tk.Label(ventana, 
                 text="MI LISTA PERSONAL",
                 font=("Arial", 18, "bold"),
                 bg="lightblue",
                 fg="darkblue")
titulo.pack(pady=10)


cuadro_frame = tk.Frame(ventana, bg="lightblue")
cuadro_frame.pack(pady=10)

tk.Label(cuadro_frame, 
        text="Escribe algo:", 
        font=("Arial", 12),
        bg="lightblue").pack(side="left", padx=5)

entrada_texto = tk.Entry(cuadro_frame, 
                        font=("Arial", 12), 
                        width=20)
entrada_texto.pack(side="left", padx=5)
entrada_texto.focus() 

# Botones
botones_frame = tk.Frame(ventana, bg="lightblue")
botones_frame.pack(pady=10)

boton_agregar = tk.Button(botones_frame,
                         text="Agregar a la Lista",
                         command=agregar_item,
                         font=("Arial", 10),
                         bg="green",
                         fg="white",
                         width=15)
boton_agregar.pack(side="left", padx=5)

boton_borrar = tk.Button(botones_frame,
                        text="Borrar Seleccionado",
                        command=borrar_item,
                        font=("Arial", 10),
                        bg="red",
                        fg="white",
                        width=15)
boton_borrar.pack(side="left", padx=5)

marco_lista = tk.Frame(ventana)
marco_lista.pack(pady=10, padx=20)

lista_elementos = tk.Listbox(marco_lista,
                           font=("Arial", 12),
                           height=10,
                           width=30,
                           selectbackground="yellow")
lista_elementos.pack(side="left")


scrollbar = tk.Scrollbar(marco_lista)
scrollbar.pack(side="right", fill="y")


lista_elementos.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=lista_elementos.yview)


elementos_ejemplo = ["Comprar leche", "Hacer tarea", "Llamar a mamá", "Ir al gimnasio"]
for item in elementos_ejemplo:
    lista_elementos.insert(tk.END, item)


etiqueta_contador = tk.Label(ventana,
                           text=f"Hay {lista_elementos.size()} elementos",
                           font=("Arial", 11, "bold"),
                           bg="lightblue",
                           fg="darkred")
etiqueta_contador.pack(pady=10)


instrucciones = tk.Label(ventana,
                        text="Instrucciones:\n1. Escribe en el cuadro de arriba\n2. Pulsa 'Agregar a la Lista'\n3. Para borrar, selecciona y pulsa 'Borrar'",
                        font=("Arial", 9),
                        bg="lightblue",
                        fg="darkgreen",
                        justify="left")
instrucciones.pack(pady=10)


ventana.mainloop()