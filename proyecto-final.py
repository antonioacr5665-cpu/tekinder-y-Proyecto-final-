import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import csv

# Clase principal del sistema
class SistemaMonitoreoAccesos:
    def __init__(self):
        self.usuarios = ["admin", "usuario1", "usuario2", "usuario3", "invitado"]
        self.servidores = ["Servidor_Principal", "Servidor_Backup", "Servidor_BD", "Servidor_Web"]
        self.tipos_acceso = ["Éxito", "Fallido", "Bloqueado", "Sospechoso"]
        
        # Matrices para almacenar datos 
        self.intentos = []  
        self.IPs = []       
        self.tipos = []     
        self.horas = []     
        
        self.inicializar_matrices_vacias()
        
        # Crear interfaz
        self.crear_interfaz()
    
    def inicializar_matrices_vacias(self):
        """Inicializa las matrices vacías sin datos de ejemplo"""

        self.intentos = [[0 for _ in self.servidores] for _ in self.usuarios]
        self.IPs = [["" for _ in self.servidores] for _ in self.usuarios]
        self.tipos = [["" for _ in self.servidores] for _ in self.usuarios]
        self.horas = [["" for _ in self.servidores] for _ in self.usuarios]
    
    def registrar_intento(self, usuario, servidor, tipo, ip, hora=None):
        """Registra un nuevo intento de acceso"""
        try:
            if usuario not in self.usuarios:
                self.usuarios.append(usuario)

                for matriz in [self.intentos, self.IPs, self.tipos, self.horas]:
                    matriz.append([0 if matriz == self.intentos else "" for _ in self.servidores])
            
            if servidor not in self.servidores:
                self.servidores.append(servidor)
  
                for i in range(len(self.usuarios)):
                    for matriz in [self.intentos, self.IPs, self.tipos, self.horas]:
                        if matriz == self.intentos:
                            matriz[i].append(0)
                        else:
                            matriz[i].append("")
            
            usuario_idx = self.usuarios.index(usuario)
            servidor_idx = self.servidores.index(servidor)
            
            # Actualizar datos
            self.intentos[usuario_idx][servidor_idx] += 1
            self.IPs[usuario_idx][servidor_idx] = ip
            self.tipos[usuario_idx][servidor_idx] = tipo
            self.horas[usuario_idx][servidor_idx] = hora if hora else datetime.now().strftime("%H:%M")

            self.generar_alertas(usuario, servidor, tipo, ip)
            
            return True
        except Exception as e:
            print(f"Error al registrar intento: {e}")
            return False
    
    def generar_alertas(self, usuario, servidor, tipo, ip):
        """Genera alertas basadas en patrones sospechosos"""
        alertas = []
        
        if tipo == "Bloqueado":
            alertas.append(f"ALERTA: Acceso bloqueado para {usuario} en {servidor}")
        
        if tipo == "Sospechoso":
            alertas.append(f"ALERTA CRÍTICA: Acceso sospechoso detectado para {usuario} en {servidor}")

        if "192.168.1.100" in ip or "10.0.0.15" in ip:
            alertas.append(f"ALERTA: IP sospechosa detectada ({ip}) para {usuario}")
        
        usuario_idx = self.usuarios.index(usuario) if usuario in self.usuarios else -1
        if usuario_idx != -1:
            intentos_totales = sum(self.intentos[usuario_idx])
            if intentos_totales > 15:
                alertas.append(f"ALERTA: {usuario} tiene {intentos_totales} intentos de acceso")
        
        return alertas
    
    def mostrar_reporte(self, filtro_usuario=None, filtro_servidor=None):
        """Genera un reporte de accesos con filtros opcionales"""
        reporte = "=== REPORTE DE ACCESOS ===\n\n"
        
        total_intentos = sum(sum(fila) for fila in self.intentos)
        reporte += f"Total de intentos de acceso: {total_intentos}\n"
        
        if total_intentos == 0:
            reporte += "\nNo hay intentos de acceso registrados.\n"
            reporte += "Registre un intento para comenzar a monitorear.\n"
            return reporte
        
        conteo_tipos = {tipo: 0 for tipo in self.tipos_acceso}
        tipos_presentes = False
        
        for i in range(len(self.usuarios)):
            for j in range(len(self.servidores)):
                tipo = self.tipos[i][j]
                if tipo and tipo in conteo_tipos:  # Verificar que no esté vacío
                    conteo_tipos[tipo] += self.intentos[i][j]
                    if self.intentos[i][j] > 0:
                        tipos_presentes = True
        
        if tipos_presentes:
            reporte += "\nDistribución por tipo de acceso:\n"
            for tipo, cantidad in conteo_tipos.items():
                if cantidad > 0:
                    porcentaje = (cantidad / total_intentos * 100) if total_intentos > 0 else 0
                    reporte += f"  {tipo}: {cantidad} ({porcentaje:.1f}%)\n"
        
        # Detalles por usuario
        reporte += "\nDetalles por usuario:\n"
        usuarios_con_datos = False
        
        for i, usuario in enumerate(self.usuarios):
            if filtro_usuario and filtro_usuario != usuario:
                continue
                
            intentos_usuario = sum(self.intentos[i])
            if intentos_usuario > 0:
                usuarios_con_datos = True
                reporte += f"\n  Usuario: {usuario} (Total: {intentos_usuario})\n"
                
                for j, servidor in enumerate(self.servidores):
                    if filtro_servidor and filtro_servidor != servidor:
                        continue
                        
                    if self.intentos[i][j] > 0 and self.tipos[i][j]:  # Verificar que haya tipo
                        reporte += f"    - {servidor}: {self.intentos[i][j]} intentos"
                        reporte += f", Último: {self.tipos[i][j]}"
                        
                        if self.horas[i][j]:
                            reporte += f" a las {self.horas[i][j]}"
                        
                        if self.IPs[i][j]:
                            reporte += f" desde {self.IPs[i][j]}\n"
                        else:
                            reporte += "\n"
        
        if not usuarios_con_datos:
            reporte += "\nNo hay datos de acceso para mostrar con los filtros seleccionados.\n"
        
    
        alertas = []
        for i, usuario in enumerate(self.usuarios):
            for j, servidor in enumerate(self.servidores):
                if self.tipos[i][j] in ["Bloqueado", "Sospechoso"]:
                    alertas.append(f"{usuario} en {servidor}: {self.tipos[i][j]}")
        
        if alertas:
            reporte += "\n=== ALERTAS ACTIVAS ===\n"
            for alerta in alertas:
                reporte += f"- {alerta}\n"
        
        return reporte
    
    def generar_grafico(self):
        """Genera un gráfico de intentos por servidor"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        
        # Gráfico 1: Intentos por servidor
        intentos_por_servidor = [sum(self.intentos[i][j] for i in range(len(self.usuarios))) 
                                for j in range(len(self.servidores))]
        
        # Verificar si hay datos para graficar
        if sum(intentos_por_servidor) > 0:
            ax1.bar(self.servidores, intentos_por_servidor, color='skyblue')
            ax1.set_title('Intentos de acceso por servidor')
            ax1.set_ylabel('Número de intentos')
            ax1.tick_params(axis='x', rotation=45)
        else:
            ax1.text(0.5, 0.5, 'No hay datos para mostrar', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax1.transAxes, fontsize=12)
            ax1.set_title('Sin datos disponibles')
        
        # Gráfico 2: Distribución por tipo
        tipos_conteo = {tipo: 0 for tipo in self.tipos_acceso}
        for i in range(len(self.usuarios)):
            for j in range(len(self.servidores)):
                tipo = self.tipos[i][j]
                if tipo and tipo in tipos_conteo:  # Verificar que no esté vacío
                    tipos_conteo[tipo] += self.intentos[i][j]
        
        # Filtrar tipos con datos
        tipos_con_datos = {k: v for k, v in tipos_conteo.items() if v > 0}
        
        if tipos_con_datos:
            colors = ['green', 'red', 'orange', 'purple']
            ax2.pie(tipos_con_datos.values(), labels=tipos_con_datos.keys(), 
                   autopct='%1.1f%%', colors=colors[:len(tipos_con_datos)])
            ax2.set_title('Distribución por tipo de acceso')
        else:
            ax2.text(0.5, 0.5, 'No hay datos para mostrar', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax2.transAxes, fontsize=12)
            ax2.set_title('Sin datos disponibles')
        
        plt.tight_layout()
        return fig
    
    def exportar_csv(self, filename):
        """Exporta los datos a un archivo CSV"""
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
           
                writer.writerow(['Usuario', 'Servidor', 'Intentos', 'Tipo', 'IP', 'Última hora'])
                
                # Datos
                datos_exportados = False
                for i, usuario in enumerate(self.usuarios):
                    for j, servidor in enumerate(self.servidores):
                        if self.intentos[i][j] > 0 and self.tipos[i][j]:
                            datos_exportados = True
                            writer.writerow([
                                usuario,
                                servidor,
                                self.intentos[i][j],
                                self.tipos[i][j],
                                self.IPs[i][j],
                                self.horas[i][j]
                            ])
                
                if not datos_exportados:
                    writer.writerow(['No hay datos registrados', '', '', '', '', ''])
            
            return True
        except Exception as e:
            print(f"Error al exportar CSV: {e}")
            return False
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica del sistema"""
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Monitoreo de Accesos")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg='#f0f0f0')

        titulo = tk.Label(self.ventana, text="Sistema de Monitoreo de Accesos", 
                         font=("Arial", 20, "bold"), bg='#2c3e50', fg='white')
        titulo.pack(fill=tk.X, padx=10, pady=10)

        marco_principal = ttk.Frame(self.ventana)
        marco_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        panel_izquierdo = ttk.Frame(marco_principal)
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
   
        panel_derecho = ttk.Frame(marco_principal)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # CONTROLES EN PANEL IZQUIERDO 

        marco_registro = ttk.LabelFrame(panel_izquierdo, text="Registrar nuevo intento", padding=10)
        marco_registro.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(marco_registro, text="Usuario:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_usuario = ttk.Entry(marco_registro, width=20)
        self.entry_usuario.grid(row=0, column=1, pady=5)
    

        ttk.Label(marco_registro, text="Servidor:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.combo_servidor = ttk.Combobox(marco_registro, values=self.servidores, width=18)
        self.combo_servidor.grid(row=1, column=1, pady=5)
        self.combo_servidor.set("")  # Dejar vacío inicialmente
     
        ttk.Label(marco_registro, text="Tipo:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.combo_tipo = ttk.Combobox(marco_registro, values=self.tipos_acceso, width=18)
        self.combo_tipo.grid(row=2, column=1, pady=5)
        self.combo_tipo.set("")  # Dejar vacío inicialmente
        
       
        ttk.Label(marco_registro, text="IP:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_ip = ttk.Entry(marco_registro, width=20)
        self.entry_ip.grid(row=3, column=1, pady=5)
       
   
        btn_registrar = ttk.Button(marco_registro, text="Registrar Intento", 
                                  command=self.registrar_intento_gui)
        btn_registrar.grid(row=4, column=0, columnspan=2, pady=10)

        marco_filtros = ttk.LabelFrame(panel_izquierdo, text="Filtros para reporte", padding=10)
        marco_filtros.pack(fill=tk.X, padx=5, pady=10)
        
   
        ttk.Label(marco_filtros, text="Filtrar por usuario:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.combo_filtro_usuario = ttk.Combobox(marco_filtros, values=["Todos"] + self.usuarios, width=18)
        self.combo_filtro_usuario.grid(row=0, column=1, pady=5)
        self.combo_filtro_usuario.set("Todos")
        
 
        ttk.Label(marco_filtros, text="Filtrar por servidor:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.combo_filtro_servidor = ttk.Combobox(marco_filtros, values=["Todos"] + self.servidores, width=18)
        self.combo_filtro_servidor.grid(row=1, column=1, pady=5)
        self.combo_filtro_servidor.set("Todos")
        
      
        marco_botones = ttk.Frame(panel_izquierdo)
        marco_botones.pack(fill=tk.X, padx=5, pady=10)
        
        btn_generar_reporte = ttk.Button(marco_botones, text="Generar Reporte", 
                                        command=self.mostrar_reporte_gui)
        btn_generar_reporte.pack(side=tk.LEFT, padx=2)
        
        btn_grafico = ttk.Button(marco_botones, text="Ver Gráfico", 
                                command=self.mostrar_grafico_gui)
        btn_grafico.pack(side=tk.LEFT, padx=2)
        
        btn_exportar = ttk.Button(marco_botones, text="Exportar CSV", 
                                 command=self.exportar_csv_gui)
        btn_exportar.pack(side=tk.LEFT, padx=2)
        
        btn_simular = ttk.Button(marco_botones, text="Simular Datos", 
                                command=self.simular_datos)
        btn_simular.pack(side=tk.LEFT, padx=2)
        

        marco_alertas = ttk.LabelFrame(panel_izquierdo, text="Alertas Recientes", padding=10)
        marco_alertas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.texto_alertas = scrolledtext.ScrolledText(marco_alertas, height=10)
        self.texto_alertas.pack(fill=tk.BOTH, expand=True)
        
 
        self.texto_alertas.insert(tk.END, "No hay alertas activas.\n")
        self.texto_alertas.insert(tk.END, "Registre un intento de acceso para comenzar.\n")
        
    #VISUALIZACIÓN EN PANEL DERECHO 

        notebook = ttk.Notebook(panel_derecho)
        notebook.pack(fill=tk.BOTH, expand=True)
        

        pestaña_reporte = ttk.Frame(notebook)
        notebook.add(pestaña_reporte, text="Reporte Detallado")
        
        self.texto_reporte = scrolledtext.ScrolledText(pestaña_reporte, wrap=tk.WORD)
        self.texto_reporte.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        

        self.texto_reporte.insert(tk.END, "=== SISTEMA DE MONITOREO DE ACCESOS ===\n\n")
        self.texto_reporte.insert(tk.END, "Bienvenido al sistema de monitoreo.\n\n")
        self.texto_reporte.insert(tk.END, "Para comenzar:\n")
        self.texto_reporte.insert(tk.END, "1. Complete los campos en 'Registrar nuevo intento'\n")
        self.texto_reporte.insert(tk.END, "2. Haga clic en 'Registrar Intento'\n")
        self.texto_reporte.insert(tk.END, "3. Genere reportes usando los filtros disponibles\n\n")
        self.texto_reporte.insert(tk.END, "No hay datos registrados aún.\n")

        pestaña_matriz = ttk.Frame(notebook)
        notebook.add(pestaña_matriz, text="Vista de Matriz")
        

        self.crear_tabla_matriz(pestaña_matriz)

        pestaña_graficos = ttk.Frame(notebook)
        notebook.add(pestaña_graficos, text="Gráficos")
        

    
    def crear_tabla_matriz(self, parent):
        """Crea una tabla para mostrar la matriz de intentos"""

        columnas = ["Usuario"] + self.servidores
        self.tabla_matriz = ttk.Treeview(parent, columns=columnas, show="headings", height=15)
        
   
        for col in columnas:
            self.tabla_matriz.heading(col, text=col)
            self.tabla_matriz.column(col, width=100, anchor=tk.CENTER)
        

        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tabla_matriz.yview)
        self.tabla_matriz.configure(yscrollcommand=scrollbar.set)
 
        self.tabla_matriz.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        

        self.actualizar_tabla_matriz()
    
    def actualizar_tabla_matriz(self):
        """Actualiza los datos en la tabla de matriz"""
      
        for item in self.tabla_matriz.get_children():
            self.tabla_matriz.delete(item)
        
  
        for i, usuario in enumerate(self.usuarios):
            valores = [usuario]
            for j in range(len(self.servidores)):
                valores.append(self.intentos[i][j])
            self.tabla_matriz.insert("", tk.END, values=valores)
    
    def registrar_intento_gui(self):
        """Maneja el registro de intentos desde la GUI"""
        usuario = self.entry_usuario.get()
        servidor = self.combo_servidor.get()
        tipo = self.combo_tipo.get()
        ip = self.entry_ip.get()
        
        if not usuario or not servidor or not tipo or not ip:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos")
            return
        
     
        if self.registrar_intento(usuario, servidor, tipo, ip):
            messagebox.showinfo("Éxito", "Intento registrado correctamente")
            
           
            self.entry_usuario.delete(0, tk.END)
            self.combo_servidor.set("")
            self.combo_tipo.set("")
            self.entry_ip.delete(0, tk.END)
            
        
            self.actualizar_tabla_matriz()
            self.actualizar_alertas()
            self.mostrar_reporte_gui()
        else:
            messagebox.showerror("Error", "No se pudo registrar el intento")
    
    def mostrar_reporte_gui(self):
        """Muestra el reporte en la GUI"""
   
        filtro_usuario = None if self.combo_filtro_usuario.get() == "Todos" else self.combo_filtro_usuario.get()
        filtro_servidor = None if self.combo_filtro_servidor.get() == "Todos" else self.combo_filtro_servidor.get()

        reporte = self.mostrar_reporte(filtro_usuario, filtro_servidor)
        
    
        self.texto_reporte.delete(1.0, tk.END)
        self.texto_reporte.insert(tk.END, reporte)
    
    def mostrar_grafico_gui(self):
        """Muestra el gráfico en una ventana emergente"""
       
        ventana_grafico = tk.Toplevel(self.ventana)
        ventana_grafico.title("Gráficos de Accesos")
        ventana_grafico.geometry("800x500")
        
        # Generar gráfico
        fig = self.generar_grafico()
        
        # Integrar gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
      
        btn_cerrar = ttk.Button(ventana_grafico, text="Cerrar", 
                               command=ventana_grafico.destroy)
        btn_cerrar.pack(pady=10)
    
    def exportar_csv_gui(self):
        """Exporta los datos a CSV desde la GUI"""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Guardar reporte como CSV"
        )
        
        if filename:
            if self.exportar_csv(filename):
                messagebox.showinfo("Éxito", f"Reporte exportado a {filename}")
            else:
                messagebox.showerror("Error", "No se pudo exportar el reporte")
    
    def simular_datos(self):
        """Simula múltiples intentos de acceso para probar el sistema"""
        
        respuesta = simpledialog.askinteger("Simular datos", 
                                           "¿Cuántos intentos desea simular?",
                                           minvalue=1, maxvalue=50)
        
        if respuesta:
            for _ in range(respuesta):
                usuario = random.choice(self.usuarios)
                servidor = random.choice(self.servidores)
                tipo = random.choice(self.tipos_acceso)
                ip = f"192.168.{random.randint(1,255)}.{random.randint(1,254)}"
                
                self.registrar_intento(usuario, servidor, tipo, ip)
            
        
            self.actualizar_tabla_matriz()
            self.actualizar_alertas()
            self.mostrar_reporte_gui()
            
            messagebox.showinfo("Simulación", f"Se han simulado {respuesta} intentos de acceso")
    
    def actualizar_alertas(self):
        """Actualiza el área de alertas en la GUI"""
        self.texto_alertas.delete(1.0, tk.END)
        
        
        alertas_totales = []
        for i, usuario in enumerate(self.usuarios):
            for j, servidor in enumerate(self.servidores):
                if self.tipos[i][j]:  # Solo si hay tipo registrado
                    alertas = self.generar_alertas(usuario, servidor, 
                                                  self.tipos[i][j], self.IPs[i][j])
                    alertas_totales.extend(alertas)
        
        
        alertas_unicas = list(set(alertas_totales))
        if alertas_unicas:
            self.texto_alertas.insert(tk.END, "=== ALERTAS ACTIVAS ===\n\n")
            for alerta in alertas_unicas:
                self.texto_alertas.insert(tk.END, f"• {alerta}\n")
        else:
         
            total_intentos = sum(sum(fila) for fila in self.intentos)
            if total_intentos > 0:
                self.texto_alertas.insert(tk.END, "No hay alertas activas.\n")
                self.texto_alertas.insert(tk.END, f"Total de intentos registrados: {total_intentos}\n")
            else:
                self.texto_alertas.insert(tk.END, "No hay alertas activas.\n")
                self.texto_alertas.insert(tk.END, "Registre un intento de acceso para comenzar.\n")
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        self.ventana.mainloop()


# Función para mostrar manual de uso
def mostrar_manual():
    manual = """
    MANUAL DE USO - SISTEMA DE MONITOREO DE ACCESOS 
    
    1. REGISTRAR NUEVO INTENTO:
       - Complete los campos: Usuario, Servidor, Tipo e IP
       - Haga clic en "Registrar Intento"
    
    2. GENERAR REPORTES:
       - Seleccione filtros opcionales (usuario y servidor)
       - Haga clic en "Generar Reporte"
    
    3. VISUALIZAR DATOS:
       - Use las pestañas para cambiar entre:
         * Reporte Detallado: Informe textual completo
         * Vista de Matriz: Tabla de intentos por usuario/servidor
         * Gráficos: Visualizaciones gráficas
    
    4. OTRAS FUNCIONES:
       - "Ver Gráfico": Muestra gráficos en ventana emergente
       - "Exportar CSV": Guarda datos en archivo CSV
       - "Simular Datos": Genera datos de prueba
       
    5. ALERTAS:
       - El sistema genera alertas automáticas para:
         * Accesos bloqueados o sospechosos
         * IPs sospechosas
         * Múltiples intentos de acceso
    
    ===== ESTADO INICIAL =====
    - Al iniciar el sistema, las alertas y reportes estarán vacíos
    - Debe registrar al menos un intento de acceso para ver datos
    - Use "Simular Datos" para probar rápidamente el sistema
    """
    
    ventana_manual = tk.Tk()
    ventana_manual.title("Manual de Uso")
    ventana_manual.geometry("700x600")
    
    texto_manual = scrolledtext.ScrolledText(ventana_manual, wrap=tk.WORD, font=("Arial", 10))
    texto_manual.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    texto_manual.insert(tk.END, manual)
    texto_manual.config(state=tk.DISABLED)
    
    btn_cerrar = ttk.Button(ventana_manual, text="Cerrar", command=ventana_manual.destroy)
    btn_cerrar.pack(pady=10)
    
    ventana_manual.mainloop()


# Punto de entrada del programa
if __name__ == "__main__":
    print("Iniciando Sistema de Monitoreo de Accesos...")
    
    # Preguntar si mostrar el manual primero
    respuesta = input("¿Desea ver el manual de uso antes de iniciar? (s/n): ")
    
    if respuesta.lower() == 's':
        mostrar_manual()
    
    sistema = SistemaMonitoreoAccesos()
    sistema.ejecutar()