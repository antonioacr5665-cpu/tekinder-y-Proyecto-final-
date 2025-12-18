import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class SistemaGestionArticulos:
    def __init__(self):
        # Configuración de la base de datos
        self.config_db = {
            'host': 'localhost',
            'user': 'root',  
            'password': 'A30/C11/r00*',  
            'database': 'gestion_articulos'
        }
        
        # Conectar a la base de datos
        self.conexion = self.conectar_bd()
        
        # Crear interfaz gráfica
        self.crear_interfaz()
    
    def conectar_bd(self):
        """Establece conexión con la base de datos MySQL"""
        try:
            conexion = mysql.connector.connect(**self.config_db)
            if conexion.is_connected():
                print("Conexión exitosa a la base de datos")
                return conexion
        except Error as e:
            messagebox.showerror("Error de Conexión", 
                                f"No se pudo conectar a la base de datos:\n{str(e)}")
            return None
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica principal"""
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Gestión de Artículos")
        self.ventana.geometry("1000x600")
        self.ventana.configure(bg='#2c3e50')
        
        # Título principal
        titulo_frame = tk.Frame(self.ventana, bg='#1a252f', height=80)
        titulo_frame.pack(fill=tk.X)
        titulo_frame.pack_propagate(False)
        
        titulo = tk.Label(titulo_frame, 
                         text="SISTEMA DE GESTIÓN DE ARTÍCULOS", 
                         font=("Arial", 20, "bold"), 
                         bg='#1a252f', 
                         fg='white')
        titulo.pack(pady=20)
        
        # Frame principal con pestañas
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear las pestañas
        self.crear_pestana_carga()
        self.crear_pestana_consulta()
        self.crear_pestana_listado()
        
        # Barra de estado
        self.barra_estado = tk.Label(self.ventana, 
                                    text="Conectado a la base de datos | Sistema listo", 
                                    bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                    bg='#34495e', fg='white')
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)
    
    def crear_pestana_carga(self):
        """Crea la pestaña para cargar nuevos artículos"""
        pestana = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(pestana, text="Carga de Artículos")
        
        # Frame para el formulario
        formulario_frame = tk.Frame(pestana, bg='white', bd=2, relief=tk.RIDGE)
        formulario_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Título del formulario
        titulo_form = tk.Label(formulario_frame, 
                              text="NUEVO ARTÍCULO", 
                              font=("Arial", 16, "bold"), 
                              bg='white', fg='#2c3e50')
        titulo_form.pack(pady=20)
        
        # Campos del formulario
        campos = [
            ("Código del Artículo:", "entry_codigo"),
            ("Descripción:", "entry_descripcion"),
            ("Precio ($):", "entry_precio")
        ]
        
        for i, (texto, nombre) in enumerate(campos):
            frame_campo = tk.Frame(formulario_frame, bg='white')
            frame_campo.pack(fill=tk.X, padx=30, pady=10)
            
            label = tk.Label(frame_campo, text=texto, 
                            font=("Arial", 11), 
                            bg='white', width=20, anchor='w')
            label.pack(side=tk.LEFT)
            
            if nombre == "entry_descripcion":
                entry = tk.Text(frame_campo, height=4, width=40, font=("Arial", 10))
            else:
                entry = tk.Entry(frame_campo, width=40, font=("Arial", 10))
            
            entry.pack(side=tk.LEFT, padx=10)
            setattr(self, nombre, entry)
        
        # Botones
        botones_frame = tk.Frame(formulario_frame, bg='white')
        botones_frame.pack(pady=30)
        
        btn_guardar = tk.Button(botones_frame, 
                               text="GUARDAR ARTÍCULO", 
                               command=self.guardar_articulo,
                               bg='#27ae60', fg='white',
                               font=("Arial", 11, "bold"),
                               width=20, height=2)
        btn_guardar.pack(side=tk.LEFT, padx=10)
        
        btn_limpiar = tk.Button(botones_frame, 
                               text="LIMPIAR FORMULARIO", 
                               command=self.limpiar_formulario,
                               bg='#e67e22', fg='white',
                               font=("Arial", 11, "bold"),
                               width=20, height=2)
        btn_limpiar.pack(side=tk.LEFT, padx=10)
        
    
    def crear_pestana_consulta(self):
        """Crea la pestaña para consultar artículos por código"""
        pestana = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(pestana, text="Consulta por Código")
        
        # Frame para búsqueda
        busqueda_frame = tk.Frame(pestana, bg='white', bd=2, relief=tk.RIDGE)
        busqueda_frame.pack(pady=20, padx=20, fill=tk.X)
        
        # Título
        titulo = tk.Label(busqueda_frame, 
                         text="BUSCAR ARTÍCULO", 
                         font=("Arial", 16, "bold"), 
                         bg='white', fg='#2c3e50')
        titulo.pack(pady=20)
        
        # Campo de búsqueda
        frame_codigo = tk.Frame(busqueda_frame, bg='white')
        frame_codigo.pack(pady=10)
        
        label_codigo = tk.Label(frame_codigo, 
                               text="Código del Artículo:", 
                               font=("Arial", 11), 
                               bg='white', width=20)
        label_codigo.pack(side=tk.LEFT)
        
        self.entry_busqueda = tk.Entry(frame_codigo, width=40, font=("Arial", 10))
        self.entry_busqueda.pack(side=tk.LEFT, padx=10)
        
        # Botón de búsqueda
        btn_buscar = tk.Button(frame_codigo, 
                              text="BUSCAR", 
                              command=self.buscar_articulo,
                              bg='#3498db', fg='white',
                              font=("Arial", 10, "bold"),
                              width=15)
        btn_buscar.pack(side=tk.LEFT, padx=10)
        
        # Frame para resultados
        resultados_frame = tk.Frame(pestana, bg='white', bd=2, relief=tk.RIDGE)
        resultados_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Etiquetas de resultados
        self.labels_resultado = {}
        campos_resultado = [
            ("Código:", "codigo_result"),
            ("Descripción:", "desc_result"),
            ("Precio:", "precio_result"),
            ("Fecha Registro:", "fecha_result")
        ]
        
        for i, (texto, nombre) in enumerate(campos_resultado):
            frame = tk.Frame(resultados_frame, bg='white')
            frame.pack(fill=tk.X, padx=30, pady=15)
            
            label = tk.Label(frame, text=texto, 
                            font=("Arial", 11, "bold"), 
                            bg='white', width=15, anchor='w')
            label.pack(side=tk.LEFT)
            
            valor = tk.Label(frame, text="", 
                            font=("Arial", 11), 
                            bg='white', fg='#2c3e50',
                            width=40, anchor='w')
            valor.pack(side=tk.LEFT)
            
            self.labels_resultado[nombre] = valor
        
        # Botones adicionales
        botones_frame = tk.Frame(resultados_frame, bg='white')
        botones_frame.pack(pady=30)
        
        btn_editar = tk.Button(botones_frame, 
                              text="EDITAR ARTÍCULO", 
                              command=self.editar_articulo,
                              bg='#9b59b6', fg='white',
                              font=("Arial", 10, "bold"),
                              width=20)
        btn_editar.pack(side=tk.LEFT, padx=10)
        
        btn_eliminar = tk.Button(botones_frame, 
                                text="ELIMINAR ARTÍCULO", 
                                command=self.eliminar_articulo,
                                bg='#e74c3c', fg='white',
                                font=("Arial", 10, "bold"),
                                width=20)
        btn_eliminar.pack(side=tk.LEFT, padx=10)
    
    def crear_pestana_listado(self):
        """Crea la pestaña para listar todos los artículos"""
        pestana = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(pestana, text="Listado Completo")
        
        # Frame para controles
        controles_frame = tk.Frame(pestana, bg='white', bd=2, relief=tk.RIDGE)
        controles_frame.pack(pady=20, padx=20, fill=tk.X)
        
        # Título
        titulo = tk.Label(controles_frame, 
                         text="LISTADO DE ARTÍCULOS", 
                         font=("Arial", 16, "bold"), 
                         bg='white', fg='#2c3e50')
        titulo.pack(pady=20)
        
        # Botones de control
        botones_frame = tk.Frame(controles_frame, bg='white')
        botones_frame.pack(pady=10)
        
        btn_actualizar = tk.Button(botones_frame, 
                                  text="ACTUALIZAR LISTADO", 
                                  command=self.actualizar_listado,
                                  bg='#3498db', fg='white',
                                  font=("Arial", 10, "bold"),
                                  width=20)
        btn_actualizar.pack(side=tk.LEFT, padx=10)
        
        btn_exportar = tk.Button(botones_frame, 
                                text="EXPORTAR A CSV", 
                                command=self.exportar_csv,
                                bg='#27ae60', fg='white',
                                font=("Arial", 10, "bold"),
                                width=20)
        btn_exportar.pack(side=tk.LEFT, padx=10)
        
        btn_imprimir = tk.Button(botones_frame, 
                                text="IMPRIMIR REPORTE", 
                                command=self.imprimir_reporte,
                                bg='#e67e22', fg='white',
                                font=("Arial", 10, "bold"),
                                width=20)
        btn_imprimir.pack(side=tk.LEFT, padx=10)
        
        # Frame para la tabla
        tabla_frame = tk.Frame(pestana, bg='white')
        tabla_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Crear Treeview para mostrar los artículos
        columnas = ("ID", "Código", "Descripción", "Precio", "Fecha Registro")
        self.tree = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=15)
        
        # Configurar columnas
        anchos = [50, 100, 300, 100, 150]
        for col, ancho in zip(columnas, anchos):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor='center')
        
        # Agregar scrollbars
        scroll_y = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_x = ttk.Scrollbar(tabla_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Empaquetar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Frame para estadísticas
        stats_frame = tk.Frame(pestana, bg='#f8f9fa', bd=1, relief=tk.SUNKEN)
        stats_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.label_stats = tk.Label(stats_frame, 
                                   text="Total de artículos: 0 | Precio promedio: $0.00", 
                                   font=("Arial", 10), 
                                   bg='#f8f9fa', fg='#2c3e50')
        self.label_stats.pack(pady=10)
        
        # Cargar datos iniciales - CON VERIFICACIÓN DE SEGURIDAD
        if hasattr(self, 'barra_estado'):
            self.actualizar_listado()
        else:
            # Programar la actualización para cuando la barra ya exista
            self.ventana.after(100, self.actualizar_listado)
    
    # === FUNCIONALIDADES DE BASE DE DATOS ===
    
    def guardar_articulo(self):
        """Guarda un nuevo artículo en la base de datos"""
        # Obtener datos del formulario
        codigo = self.entry_codigo.get().strip()
        descripcion = self.entry_descripcion.get("1.0", tk.END).strip()
        precio = self.entry_precio.get().strip()
        
        # Validar campos
        if not codigo or not descripcion or not precio:
            messagebox.showwarning("Campos incompletos", 
                                  "Por favor complete todos los campos")
            return
        
        try:
            precio_float = float(precio)
            if precio_float <= 0:
                messagebox.showwarning("Precio inválido", 
                                      "El precio debe ser mayor a 0")
                return
        except ValueError:
            messagebox.showwarning("Precio inválido", 
                                  "Ingrese un precio válido (ej: 99.99)")
            return
        
        # Verificar si el código ya existe
        if self.verificar_codigo_existente(codigo):
            messagebox.showwarning("Código duplicado", 
                                  f"El código '{codigo}' ya existe en la base de datos")
            return
        
        # Insertar en la base de datos
        try:
            cursor = self.conexion.cursor()
            query = """
            INSERT INTO articulos (codigo, descripcion, precio) 
            VALUES (%s, %s, %s)
            """
            valores = (codigo, descripcion, precio_float)
            
            cursor.execute(query, valores)
            self.conexion.commit()
            
            messagebox.showinfo("Éxito", 
                              f"Artículo '{codigo}' guardado correctamente")
            
            # Limpiar formulario
            self.limpiar_formulario()
            
            # Actualizar listado
            self.actualizar_listado()
            
            # Actualizar barra de estado
            if hasattr(self, 'barra_estado'):
                self.barra_estado.config(text=f"Artículo '{codigo}' guardado | {datetime.now().strftime('%H:%M:%S')}")
            
        except Error as e:
            messagebox.showerror("Error", 
                                f"No se pudo guardar el artículo:\n{str(e)}")
    
    def verificar_codigo_existente(self, codigo):
        """Verifica si un código ya existe en la base de datos"""
        try:
            cursor = self.conexion.cursor()
            query = "SELECT COUNT(*) FROM articulos WHERE codigo = %s"
            cursor.execute(query, (codigo,))
            resultado = cursor.fetchone()
            return resultado[0] > 0
        except Error:
            return False
    
    def buscar_articulo(self):
        """Busca un artículo por su código"""
        codigo = self.entry_busqueda.get().strip()
        
        if not codigo:
            messagebox.showwarning("Campo vacío", 
                                  "Ingrese un código para buscar")
            return
        
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = """
            SELECT * FROM articulos 
            WHERE codigo = %s
            """
            cursor.execute(query, (codigo,))
            articulo = cursor.fetchone()
            
            if articulo:
                # Mostrar resultados
                self.labels_resultado['codigo_result'].config(
                    text=articulo['codigo']
                )
                self.labels_resultado['desc_result'].config(
                    text=articulo['descripcion']
                )
                self.labels_resultado['precio_result'].config(
                    text=f"${articulo['precio']:.2f}"
                )
                self.labels_resultado['fecha_result'].config(
                    text=articulo['fecha_registro'].strftime('%d/%m/%Y %H:%M')
                )
                
                # Cambiar a pestaña de consulta
                self.notebook.select(1)
                
                # Actualizar barra de estado con verificación
                if hasattr(self, 'barra_estado'):
                    self.barra_estado.config(
                        text=f"Artículo '{codigo}' encontrado | {datetime.now().strftime('%H:%M:%S')}"
                    )
            else:
                messagebox.showinfo("No encontrado", 
                                  f"No se encontró ningún artículo con código '{codigo}'")
                self.limpiar_resultados()
                
        except Error as e:
            messagebox.showerror("Error", 
                                f"No se pudo realizar la búsqueda:\n{str(e)}")
    
    def actualizar_listado(self):
        """Actualiza el listado completo de artículos"""
        try:
            # Limpiar tabla actual
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener datos de la base de datos
            cursor = self.conexion.cursor(dictionary=True)
            query = """
            SELECT id, codigo, descripcion, precio, fecha_registro 
            FROM articulos 
            ORDER BY fecha_registro DESC
            """
            cursor.execute(query)
            articulos = cursor.fetchall()
            
            # Insertar datos en la tabla
            total_precio = 0
            for articulo in articulos:
                precio = articulo['precio']
                total_precio += precio
                
                self.tree.insert("", tk.END, values=(
                    articulo['id'],
                    articulo['codigo'],
                    articulo['descripcion'][:100] + ("..." if len(articulo['descripcion']) > 100 else ""),
                    f"${precio:.2f}",
                    articulo['fecha_registro'].strftime('%d/%m/%Y %H:%M')
                ))
            
            # Actualizar estadísticas
            cantidad = len(articulos)
            promedio = total_precio / cantidad if cantidad > 0 else 0
            
            self.label_stats.config(
                text=f"Total de artículos: {cantidad} | Precio promedio: ${promedio:.2f}"
            )
            
            # Actualizar barra de estado CON VERIFICACIÓN
            if hasattr(self, 'barra_estado'):
                self.barra_estado.config(
                    text=f"Listado actualizado | {cantidad} artículos encontrados | {datetime.now().strftime('%H:%M:%S')}"
                )
            
        except Error as e:
            messagebox.showerror("Error", 
                                f"No se pudo cargar el listado:\n{str(e)}")
    
    def editar_articulo(self):
        """Permite editar un artículo encontrado"""
        codigo = self.labels_resultado['codigo_result'].cget("text")
        
        if not codigo:
            messagebox.showwarning("Sin artículo", 
                                  "No hay artículo seleccionado para editar")
            return
  
        ventana_edicion = tk.Toplevel(self.ventana)
        ventana_edicion.title(f"Editar Artículo: {codigo}")
        ventana_edicion.geometry("500x400")
        ventana_edicion.configure(bg='white')
        
  
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = "SELECT * FROM articulos WHERE codigo = %s"
            cursor.execute(query, (codigo,))
            articulo = cursor.fetchone()
            
            if not articulo:
                messagebox.showerror("Error", "Artículo no encontrado")
                ventana_edicion.destroy()
                return
            

            tk.Label(ventana_edicion, 
                    text="EDITAR ARTÍCULO", 
                    font=("Arial", 16, "bold"), 
                    bg='white', fg='#2c3e50').pack(pady=20)

            frame_desc = tk.Frame(ventana_edicion, bg='white')
            frame_desc.pack(pady=10, padx=20, fill=tk.X)
            
            tk.Label(frame_desc, text="Descripción:", 
                    font=("Arial", 11), bg='white').pack(anchor='w')
            
            text_desc = tk.Text(frame_desc, height=5, width=50)
            text_desc.pack(pady=5)
            text_desc.insert("1.0", articulo['descripcion'])

            frame_precio = tk.Frame(ventana_edicion, bg='white')
            frame_precio.pack(pady=10, padx=20, fill=tk.X)
            
            tk.Label(frame_precio, text="Precio ($):", 
                    font=("Arial", 11), bg='white').pack(anchor='w')
            
            entry_precio = tk.Entry(frame_precio, width=20, font=("Arial", 11))
            entry_precio.pack(pady=5)
            entry_precio.insert(0, str(articulo['precio']))
            

            frame_botones = tk.Frame(ventana_edicion, bg='white')
            frame_botones.pack(pady=20)
            
            def guardar_cambios():
                nueva_desc = text_desc.get("1.0", tk.END).strip()
                try:
                    nuevo_precio = float(entry_precio.get().strip())
                    
                    if nuevo_precio <= 0:
                        messagebox.showwarning("Precio inválido", 
                                              "El precio debe ser mayor a 0")
                        return
                    
                    # Actualizar en la base de datos
                    cursor = self.conexion.cursor()
                    query = """
                    UPDATE articulos 
                    SET descripcion = %s, precio = %s 
                    WHERE codigo = %s
                    """
                    cursor.execute(query, (nueva_desc, nuevo_precio, codigo))
                    self.conexion.commit()
                    
                    messagebox.showinfo("Éxito", 
                                      "Artículo actualizado correctamente")
                    
                    # Actualizar interfaz
                    self.buscar_articulo()
                    self.actualizar_listado()
                    
                    ventana_edicion.destroy()
                    
                except ValueError:
                    messagebox.showwarning("Precio inválido", 
                                          "Ingrese un precio válido")
            
            btn_guardar = tk.Button(frame_botones, 
                                   text="GUARDAR CAMBIOS", 
                                   command=guardar_cambios,
                                   bg='#27ae60', fg='white',
                                   font=("Arial", 10, "bold"))
            btn_guardar.pack(side=tk.LEFT, padx=10)
            
            btn_cancelar = tk.Button(frame_botones, 
                                    text="CANCELAR", 
                                    command=ventana_edicion.destroy,
                                    bg='#95a5a6', fg='white',
                                    font=("Arial", 10, "bold"))
            btn_cancelar.pack(side=tk.LEFT, padx=10)
            
        except Error as e:
            messagebox.showerror("Error", 
                                f"No se pudo cargar el artículo:\n{str(e)}")
            ventana_edicion.destroy()
    
    def eliminar_articulo(self):
        """Elimina un artículo de la base de datos"""
        codigo = self.labels_resultado['codigo_result'].cget("text")
        
        if not codigo:
            messagebox.showwarning("Sin artículo", 
                                  "No hay ningún artículo seleccionado")
            return

        respuesta = messagebox.askyesno(
            "Confirmar eliminación", 
            f"¿Está seguro de eliminar el artículo '{codigo}'?\nEsta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                cursor = self.conexion.cursor()
                query = "DELETE FROM articulos WHERE codigo = %s"
                cursor.execute(query, (codigo,))
                self.conexion.commit()
                
                messagebox.showinfo("Éxito", 
                                  f"Artículo '{codigo}' eliminado correctamente")
                

                self.limpiar_resultados()
                self.actualizar_listado()

                if hasattr(self, 'barra_estado'):
                    self.barra_estado.config(
                        text=f"Artículo '{codigo}' eliminado | {datetime.now().strftime('%H:%M:%S')}"
                    )
                
            except Error as e:
                messagebox.showerror("Error", 
                                    f"No se pudo eliminar el artículo:\n{str(e)}")
    
    def exportar_csv(self):
        """Exporta el listado de artículos a un archivo CSV"""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = """
            SELECT codigo, descripcion, precio, fecha_registro 
            FROM articulos 
            ORDER BY codigo
            """
            cursor.execute(query)
            articulos = cursor.fetchall()
            
            if not articulos:
                messagebox.showinfo("Sin datos", 
                                  "No hay artículos para exportar")
                return
            

            from tkinter import filedialog
            import csv
            
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Guardar listado como CSV"
            )
            
            if archivo:
                with open(archivo, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Código', 'Descripción', 'Precio', 'Fecha Registro'])
                    

                    for articulo in articulos:
                        writer.writerow([
                            articulo['codigo'],
                            articulo['descripcion'],
                            articulo['precio'],
                            articulo['fecha_registro'].strftime('%Y-%m-%d %H:%M:%S')
                        ])
                
                messagebox.showinfo("Éxito", 
                                  f"Listado exportado a:\n{archivo}")
                
                if hasattr(self, 'barra_estado'):
                    self.barra_estado.config(
                        text=f"Listado exportado a CSV | {datetime.now().strftime('%H:%M:%S')}"
                    )
                
        except Error as e:
            messagebox.showerror("Error", 
                                f"No se pudo exportar el listado:\n{str(e)}")
    
    def imprimir_reporte(self):
        """Genera un reporte imprimible"""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = """
            SELECT COUNT(*) as total, 
                   AVG(precio) as promedio, 
                   MAX(precio) as maximo,
                   MIN(precio) as minimo
            FROM articulos
            """
            cursor.execute(query)
            stats = cursor.fetchone()

            ventana_reporte = tk.Toplevel(self.ventana)
            ventana_reporte.title("Reporte de Artículos")
            ventana_reporte.geometry("600x500")

            texto_reporte = tk.Text(ventana_reporte, wrap=tk.WORD, font=("Courier", 10))
            texto_reporte.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            reporte = "=" * 60 + "\n"
            reporte += "REPORTE DE ARTÍCULOS - " + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n"
            reporte += "=" * 60 + "\n\n"
            
            reporte += "ESTADÍSTICAS:\n"
            reporte += "-" * 40 + "\n"
            reporte += f"Total de artículos: {stats['total']}\n"
            reporte += f"Precio promedio: ${stats['promedio']:.2f}\n"
            reporte += f"Precio más alto: ${stats['maximo']:.2f}\n"
            reporte += f"Precio más bajo: ${stats['minimo']:.2f}\n\n"
            
            cursor.execute("SELECT * FROM articulos ORDER BY codigo")
            articulos = cursor.fetchall()
            
            reporte += "LISTADO DETALLADO:\n"
            reporte += "-" * 40 + "\n"
            
            for articulo in articulos:
                reporte += f"\nCódigo: {articulo['codigo']}\n"
                reporte += f"Descripción: {articulo['descripcion'][:80]}...\n"
                reporte += f"Precio: ${articulo['precio']:.2f}\n"
                reporte += f"Registrado: {articulo['fecha_registro'].strftime('%d/%m/%Y')}\n"
                reporte += "-" * 40 + "\n"

            texto_reporte.insert("1.0", reporte)
            texto_reporte.config(state=tk.DISABLED)
            
            def imprimir():
                messagebox.showinfo("Imprimir", 
                                  "Funcionalidad de impresión activada\n"
                                  "El reporte está listo para imprimir.")
            
            btn_imprimir = tk.Button(ventana_reporte, 
                                    text="IMPRIMIR REPORTE", 
                                    command=imprimir,
                                    bg='#3498db', fg='white')
            btn_imprimir.pack(pady=10)
            
        except Error as e:
            messagebox.showerror("Error", 
                                f"No se pudo generar el reporte:\n{str(e)}")
    
    #  FUNCIONES AUXILIARES
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario de carga"""
        self.entry_codigo.delete(0, tk.END)
        self.entry_descripcion.delete("1.0", tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_codigo.focus()
    
    def limpiar_resultados(self):
        """Limpia los campos de resultados de búsqueda"""
        for label in self.labels_resultado.values():
            label.config(text="")
        self.entry_busqueda.delete(0, tk.END)
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        if self.conexion:
            self.ventana.mainloop()
        else:
            messagebox.showerror("Error crítico", 
                                "No se pudo conectar a la base de datos.\n"
                                "La aplicación se cerrará.")
            self.ventana.destroy()

if __name__ == "__main__":
    print("Iniciando Sistema de Gestión de Artículos...")
    

    app = SistemaGestionArticulos()
    app.ejecutar()