import tkinter as tk
from tkinter import ttk
from mensajes import question
class ListaDeCamaras(tk.Tk):
    def __init__(self, nuevos_directorios):
        super().__init__()
        self.title("Treeview Reordenable (Drag & Drop)")
        
        # Estado de arrastre
        self.drag_item = None
        self.drag_index = None
        self.target_row = None
        self.camaras = nuevos_directorios

        # 1. Configurar el Treeview
        self.tree = ttk.Treeview(self, columns=('N', 'Camara', 'Fecha | hora'), show='headings')
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        # 2. Definir Encabezados y Columnas
        self.tree.heading('N', text='N', anchor=tk.W)
        self.tree.heading('Camara', text='Camara', anchor=tk.W)
        self.tree.heading('Fecha | hora', text='Fecha | hora', anchor=tk.W)
        
        self.tree.column('N', width=50, anchor=tk.CENTER)
        self.tree.column('Camara', width=200, anchor=tk.W)
        self.tree.column('Fecha | hora', width=100, anchor=tk.CENTER)
        
        
        # 4. Enlazar eventos para Drag and Drop
        self.tree.bind('<Button-1>', self.on_start_drag)    # Al hacer clic
        self.tree.bind('<B1-Motion>', self.on_drag_motion) # Mientras se arrastra
        self.tree.bind('<ButtonRelease-1>', self.on_drop)   # Al soltar

        # 5. Botón de ejemplo para obtener selección
        ttk.Button(self, text="Confirmar", command=self.enumerar).pack(pady=5)
        ttk.Button(self, text="Actualizar").pack(pady=5)
        ttk.Button(self, text="Eliminar").pack(pady=5)
        ttk.Button(self, text="Copiar en portapapeles", command=self.copiar_listbox).pack(pady=5)

        self.cargar_camaras()



    # --- Métodos de Drag and Drop ---
    
    def on_start_drag(self, event):
        
        """Guarda el ID del elemento arrastrado."""
        # identify_row(y) devuelve el ID del ítem en la coordenada Y
        row_id = self.tree.identify_row(event.y)
        
        # Solo procedemos si el clic fue en una fila existente
        if row_id:
            # Limpiar selecciones previas y seleccionar solo el ítem arrastrado
            self.tree.selection_set(row_id)
            self.drag_item = row_id
            
            # Obtener el índice numérico para saber su posición inicial
            children = self.tree.get_children('')
            self.drag_index = children.index(self.drag_item)
        


    def on_drag_motion(self, event):
        """Borra el ítem en la posición original y lo inserta en la nueva posición."""
        if not self.drag_item:
            return

        # 1. Obtener el ítem bajo el puntero (destino del arrastre)
        self.target_row = self.tree.identify_row(event.y)
        
        

    
    def on_drop(self, event):
        #Si el ratón está sobre una fila válida diferente
        if self.target_row and self.target_row != self.drag_item:
            
            # Obtener la lista de todos los IDs para calcular el nuevo índice
            children = self.tree.get_children('')
            try:
                self.target_index = children.index(self.target_row)
            except ValueError:
                # El target_row no está en la lista principal (no debería pasar aquí)
                return
            '''
            SECCION DE ACTUALIZACION DE LA LISTA DE CAMARAS EN FORMATO DICCIONARIO
            '''
            #obtengo ruta origen y ruta destino
            ruta_seleccionada = self.camaras[self.drag_index]["nueva_ruta"]
            ruta_target = self.camaras[self.target_index]["nueva_ruta"]
            #Intercambio numeros de orden en los nombres
            self.camaras[self.drag_index]["nueva_ruta"] = ruta_seleccionada.parent / f"{str(self.target_index+1).zfill(2)} - {ruta_seleccionada.name[5:]}"
            self.camaras[self.target_index]["nueva_ruta"] = ruta_target.parent / f"{str(self.drag_index+1).zfill(2)} - {ruta_target.name[5:]}"
            #Intercambio numeros de orden en los ordenes
            self.camaras[self.drag_index]["orden"] = self.target_index + 1
            self.camaras[self.target_index]["orden"] = self.drag_index + 1
            #Intercambio los lugares en la lista de camaras 
            self.camaras[self.drag_index],self.camaras[self.target_index] = self.camaras[self.target_index],self.camaras[self.drag_index]
           
        """reinicio los datos"""
        self.drag_item = None
        self.drag_index = None
        self.target_index = None

        #VUELVO A CARGAR LA INTERFAZ CON LOS LOS DATOS ACTUALIZADOS
        self.cargar_camaras()



    def cargar_camaras(self):
        """Limpia y vuelve a cargar el Treeview con nuevos datos."""

        for item in self.tree.get_children():
            self.tree.delete(item)

        for dir in self.camaras:
            self.tree.insert('', tk.END, values=(dir["orden"], dir["nueva_ruta"].name[5:], dir["hora_fecha"].strftime("%Y-%m-%d | %H:%M:%S")))

    def enumerar(self):
        mensaje = question("Enumerar Directorios","Confirmar enumerado")
        if mensaje:
            for dir in self.camaras:
                print(f"Orden:  {dir["orden"]}")
                print(f"Ruta inicial: {dir["Ruta_inicial"]}")
                print(f"Nueva ruta del directorio: {dir["nueva_ruta"]}")
                print(f"Hora y fecha: {dir["hora_fecha"].strftime("%H:%M:%S %Y-%m-%d")}")
                print("Se eliminará: ", {dir["para_eliminar"]},"\n")
                dir["Ruta_inicial"].rename(dir["nueva_ruta"])

        pass

    def copiar_listbox(self):
        filas = []

        for item in self.tree.get_children():
            valores = self.tree.item(item, "values")
            filas.append("\t".join(map(str, valores)))

        texto = "\n".join(filas)

        self.clipboard_clear()
        self.clipboard_append(texto)